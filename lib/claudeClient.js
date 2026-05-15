const Anthropic = require('@anthropic-ai/sdk');

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const SYSTEM_PROMPT = `You are a banking compliance coverage analyst. You analyze two datasets — a regulatory questionnaire (universe of possible test questions grouped by regulation) and a 2LOD test inventory (tests actually executed) — and compute semantic coverage per regulation. Return STRICT JSON only. No prose, no markdown fences, no commentary.`;

/**
 * Build the user prompt with questionnaire and inventory data
 */
function buildUserPrompt(questionnaireRows, inventoryRows) {
  const questionnaireJSON = JSON.stringify(questionnaireRows, null, 2);
  const inventoryJSON = JSON.stringify(inventoryRows, null, 2);

  return `Compute test coverage per regulation and provide a brief executive summary.

INSTRUCTIONS:
1. Group the QUESTIONNAIRE rows by their "regulationSource" field. Each group represents the universe of possible test questions for that regulation.
2. For each questionnaire question, determine whether the INVENTORY contains at least one test that semantically addresses that question. Match by:
   - Topic overlap between the question text/description and the inventory test name/objective.
   - Citation overlap between questionnaire "citation" and inventory "regulation".
   A test does not need an exact citation match — a clear topical match is sufficient.
3. For each regulation compute:
   - totalQuestions  = count of questionnaire rows in that regulation
   - coveredQuestions = count of those questions matched by at least one inventory test
   - coveragePercent = round(coveredQuestions / totalQuestions * 100)
   - status:
       coveragePercent < 35           -> "Gap"
       35 <= coveragePercent <= 60    -> "Moderate"
       coveragePercent > 60           -> "Strong"
4. Return one object per regulation present in the questionnaire (even if coverage is 0%).
5. Provide an overall executive summary (2-3 paragraphs) that includes:
   - Overall coverage assessment across all regulations
   - Key strengths (regulations with strong coverage)
   - Critical gaps (regulations with poor coverage)
   - Recommended priorities for test development

OUTPUT SCHEMA (return JSON matching exactly this shape — no extra keys, no wrapping text):
{
  "summary": "string (2-3 paragraph executive summary)",
  "regulations": [
    {
      "regulation": "string (regulation name from questionnaire 'regulationSource')",
      "totalQuestions": number,
      "coveredQuestions": number,
      "coveragePercent": number,
      "status": "Gap" | "Moderate" | "Strong"
    }
  ]
}

QUESTIONNAIRE:
${questionnaireJSON}

INVENTORY:
${inventoryJSON}`;
}

/**
 * Analyze coverage using Claude API
 * @param {Array} questionnaireRows - Parsed questionnaire data
 * @param {Array} inventoryRows - Parsed inventory data
 * @returns {Promise<Object>} Coverage analysis results
 */
async function analyzeCoverage(questionnaireRows, inventoryRows) {
  try {
    const userPrompt = buildUserPrompt(questionnaireRows, inventoryRows);

    const response = await client.messages.create({
      model: 'claude-sonnet-4-6',
      max_tokens: 4096,
      system: SYSTEM_PROMPT,
      messages: [
        {
          role: 'user',
          content: userPrompt
        }
      ]
    });

    if (!response.content || response.content.length === 0) {
      throw new Error('Empty response from Claude API');
    }

    let responseText = response.content[0].text;

    // Strip markdown code fences if present
    responseText = responseText.replace(/```json\s*/g, '').replace(/```\s*/g, '').trim();

    // Parse JSON
    const result = JSON.parse(responseText);

    if (!result.regulations || !Array.isArray(result.regulations)) {
      throw new Error('Invalid response format: missing regulations array');
    }

    // Include the prompt in the response for transparency
    return {
      ...result,
      prompt: {
        system: SYSTEM_PROMPT,
        user: userPrompt,
        model: 'claude-sonnet-4-6'
      }
    };

  } catch (error) {
    if (error instanceof SyntaxError) {
      throw new Error(`Failed to parse Claude API response as JSON: ${error.message}`);
    }
    throw error;
  }
}

module.exports = {
  analyzeCoverage,
  buildUserPrompt,
  SYSTEM_PROMPT
};
