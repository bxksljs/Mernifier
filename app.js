const generateTestCases = require('./testcase-generator');

generateTestCases('code.js', (err, testCaseFilePath) => {
 if (err) {
    console.error('Failed to generate test cases:', err);
 } else {
    console.log('Test cases generated and saved at:', testCaseFilePath);
 }
});