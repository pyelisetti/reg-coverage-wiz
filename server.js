require('dotenv').config();
const express = require('express');
const multer = require('multer');
const path = require('path');
const { parseQuestionnaire, parseInventory } = require('./lib/parseExcel');
const { analyzeCoverage, buildUserPrompt, SYSTEM_PROMPT } = require('./lib/claudeClient');

const app = express();
const PORT = process.env.PORT || 3000;

// Configure multer for memory storage
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB limit
  }
});

// Serve static files from public directory
app.use(express.static('public'));

// Root route
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Get prompt endpoint (for displaying before analysis)
app.post('/api/get-prompt',
  upload.fields([
    { name: 'questionnaire', maxCount: 1 },
    { name: 'inventory', maxCount: 1 }
  ]),
  async (req, res) => {
    try {
      // Validate files are present
      if (!req.files || !req.files.questionnaire || !req.files.inventory) {
        return res.status(400).json({
          error: 'Both questionnaire and inventory files are required'
        });
      }

      const questionnaireFile = req.files.questionnaire[0];
      const inventoryFile = req.files.inventory[0];

      // Parse files
      let questionnaireRows, inventoryRows;

      try {
        questionnaireRows = parseQuestionnaire(questionnaireFile.buffer);
        inventoryRows = parseInventory(inventoryFile.buffer);
      } catch (parseError) {
        return res.status(400).json({
          error: `Failed to parse Excel files: ${parseError.message}`
        });
      }

      // Build and return prompt
      const userPromptText = buildUserPrompt(questionnaireRows, inventoryRows);

      res.json({
        prompt: {
          system: SYSTEM_PROMPT,
          user: userPromptText,
          model: 'claude-sonnet-4-6'
        }
      });

    } catch (error) {
      console.error('Server error:', error);
      res.status(500).json({
        error: 'Failed to generate prompt'
      });
    }
  }
);

// Analyze endpoint
app.post('/api/analyze',
  upload.fields([
    { name: 'questionnaire', maxCount: 1 },
    { name: 'inventory', maxCount: 1 }
  ]),
  async (req, res) => {
    try {
      // Validate files are present
      if (!req.files || !req.files.questionnaire || !req.files.inventory) {
        return res.status(400).json({
          error: 'Both questionnaire and inventory files are required'
        });
      }

      const questionnaireFile = req.files.questionnaire[0];
      const inventoryFile = req.files.inventory[0];

      // Validate file types
      const isXlsx = (file) => {
        const validMimes = [
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          'application/vnd.ms-excel'
        ];
        const validExts = ['.xlsx', '.xls'];
        return validMimes.includes(file.mimetype) ||
               validExts.some(ext => file.originalname.toLowerCase().endsWith(ext));
      };

      if (!isXlsx(questionnaireFile) || !isXlsx(inventoryFile)) {
        return res.status(400).json({
          error: 'Both files must be Excel files (.xlsx)'
        });
      }

      // Parse files
      let questionnaireRows, inventoryRows;

      try {
        questionnaireRows = parseQuestionnaire(questionnaireFile.buffer);
        inventoryRows = parseInventory(inventoryFile.buffer);
      } catch (parseError) {
        return res.status(400).json({
          error: `Failed to parse Excel files: ${parseError.message}`
        });
      }

      // Validate parsed data
      if (!questionnaireRows.length) {
        return res.status(400).json({
          error: 'Questionnaire file appears to be empty or invalid'
        });
      }

      if (!inventoryRows.length) {
        return res.status(400).json({
          error: 'Inventory file appears to be empty or invalid'
        });
      }

      // Call Claude API for analysis
      try {
        const result = await analyzeCoverage(questionnaireRows, inventoryRows);
        res.json(result);
      } catch (apiError) {
        console.error('Claude API error:', apiError);
        res.status(500).json({
          error: `Analysis failed: ${apiError.message}`
        });
      }

    } catch (error) {
      console.error('Server error:', error);
      res.status(500).json({
        error: 'An unexpected error occurred during analysis'
      });
    }
  }
);

// Error handling middleware
app.use((error, req, res, next) => {
  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({
        error: 'File size too large. Maximum size is 10MB'
      });
    }
    return res.status(400).json({
      error: `Upload error: ${error.message}`
    });
  }
  next(error);
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Regulatory Coverage Analyzer running at http://localhost:${PORT}`);
  console.log(`📊 Ready to analyze compliance coverage`);

  if (!process.env.ANTHROPIC_API_KEY) {
    console.warn('⚠️  WARNING: ANTHROPIC_API_KEY not set in environment');
  }
});
