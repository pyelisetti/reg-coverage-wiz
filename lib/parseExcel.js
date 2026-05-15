const XLSX = require('xlsx');

/**
 * Normalize a header key by trimming whitespace and lowercasing
 */
function normalizeKey(key) {
  return key.trim().toLowerCase().replace(/\s+/g, ' ');
}

/**
 * Parse the regulatory questionnaire Excel file
 * @param {Buffer} buffer - The Excel file buffer
 * @returns {Array} Array of questionnaire rows
 */
function parseQuestionnaire(buffer) {
  const workbook = XLSX.read(buffer, { type: 'buffer' });
  const sheetName = 'Detail';

  if (!workbook.SheetNames.includes(sheetName)) {
    throw new Error(`Sheet "${sheetName}" not found in questionnaire file`);
  }

  const worksheet = workbook.Sheets[sheetName];
  const rawData = XLSX.utils.sheet_to_json(worksheet);

  return rawData.map(row => {
    const normalized = {};
    Object.keys(row).forEach(key => {
      normalized[normalizeKey(key)] = row[key];
    });

    return {
      regulationSource: normalized['regulation source'] || '',
      questionCode: normalized['question code'] || '',
      questionText: normalized['question text'] || '',
      questionDescription: normalized['question description'] || '',
      citation: normalized['citation'] || '',
      questionCategory: normalized['question category name'] || ''
    };
  });
}

/**
 * Parse the 2LOD test inventory Excel file
 * @param {Buffer} buffer - The Excel file buffer
 * @returns {Array} Array of inventory rows
 */
function parseInventory(buffer) {
  const workbook = XLSX.read(buffer, { type: 'buffer' });
  const sheetName = 'Test Inventory';

  if (!workbook.SheetNames.includes(sheetName)) {
    throw new Error(`Sheet "${sheetName}" not found in inventory file`);
  }

  const worksheet = workbook.Sheets[sheetName];

  // Header row is row 3 (index 2), title is row 1
  const rawData = XLSX.utils.sheet_to_json(worksheet, { range: 2 });

  return rawData.map(row => {
    const normalized = {};
    Object.keys(row).forEach(key => {
      normalized[normalizeKey(key)] = row[key];
    });

    return {
      id: normalized['id'] || '',
      testName: normalized['test name'] || '',
      objective: normalized['objective'] || '',
      regulation: normalized['regulation'] || '',
      businessUnit: normalized['business unit'] || '',
      product: normalized['product'] || '',
      frequency: normalized['frequency'] || '',
      impDate: normalized['imp. date'] || normalized['imp date'] || ''
    };
  });
}

module.exports = {
  parseQuestionnaire,
  parseInventory
};
