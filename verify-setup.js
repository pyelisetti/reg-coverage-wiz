#!/usr/bin/env node

/**
 * Setup Verification Script
 * Run this to verify your installation is correct
 */

const fs = require('fs');
const path = require('path');

console.log('\n🔍 Verifying Coverage Analyzer Setup...\n');

let hasErrors = false;

// Check Node.js version
const nodeVersion = process.version;
const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
console.log(`✓ Node.js version: ${nodeVersion}`);
if (majorVersion < 20) {
  console.log(`  ⚠️  Warning: Node.js 20+ recommended, you have ${nodeVersion}`);
}

// Check for required files
const requiredFiles = [
  'package.json',
  'server.js',
  'lib/parseExcel.js',
  'lib/claudeClient.js',
  'public/index.html',
  'public/styles.css',
  'public/app.js',
  '.env.example'
];

console.log('\n📁 Checking required files...');
requiredFiles.forEach(file => {
  if (fs.existsSync(path.join(__dirname, file))) {
    console.log(`  ✓ ${file}`);
  } else {
    console.log(`  ✗ Missing: ${file}`);
    hasErrors = true;
  }
});

// Check for .env file
console.log('\n🔑 Checking environment configuration...');
if (fs.existsSync(path.join(__dirname, '.env'))) {
  console.log('  ✓ .env file exists');

  // Check if API key is configured
  const envContent = fs.readFileSync(path.join(__dirname, '.env'), 'utf8');
  if (envContent.includes('ANTHROPIC_API_KEY=sk-ant-')) {
    console.log('  ✓ ANTHROPIC_API_KEY appears to be set');
  } else if (envContent.includes('ANTHROPIC_API_KEY=')) {
    console.log('  ⚠️  .env file exists but API key may not be configured');
    console.log('     Update .env with your actual Claude API key');
  }
} else {
  console.log('  ✗ .env file not found');
  console.log('     Run: cp .env.example .env');
  console.log('     Then edit .env and add your Claude API key');
  hasErrors = true;
}

// Check for node_modules
console.log('\n📦 Checking dependencies...');
if (fs.existsSync(path.join(__dirname, 'node_modules'))) {
  console.log('  ✓ node_modules directory exists');

  // Check for key dependencies
  const dependencies = [
    'express',
    'multer',
    'xlsx',
    '@anthropic-ai/sdk',
    'dotenv'
  ];

  dependencies.forEach(dep => {
    const depPath = path.join(__dirname, 'node_modules', dep);
    if (fs.existsSync(depPath)) {
      console.log(`  ✓ ${dep}`);
    } else {
      console.log(`  ✗ Missing: ${dep}`);
      hasErrors = true;
    }
  });
} else {
  console.log('  ✗ node_modules not found');
  console.log('     Run: npm install');
  hasErrors = true;
}

// Final summary
console.log('\n' + '='.repeat(50));
if (hasErrors) {
  console.log('❌ Setup incomplete - please address the issues above');
  console.log('\nQuick fix:');
  console.log('  1. Run: npm install');
  console.log('  2. Run: cp .env.example .env');
  console.log('  3. Edit .env and add your Claude API key');
  process.exit(1);
} else {
  console.log('✅ Setup verification complete!');
  console.log('\nNext steps:');
  console.log('  1. Ensure .env has your Claude API key');
  console.log('  2. Run: npm start');
  console.log('  3. Open: http://localhost:3000');
  console.log('\n📖 See README.md for detailed usage instructions');
  process.exit(0);
}
