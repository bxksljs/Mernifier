const express = require('express');
const bodyParser = require('body-parser');
const { transform } = require('@babel/core');
const traverse = require('@babel/traverse').default;
const fs = require('fs');

const app = express();
const port = 3000;
module.exports = app;

app.use(bodyParser.text());

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

app.post('/generate', (req, res) => {
  const userCode = req.body;
  const testCases = generateTestCases(userCode);
  res.send(testCases);
});

function generateTestCases(inputCode) {
  const ast = transform(inputCode, {
    presets: ['@babel/preset-env', '@babel/preset-react'],
  }).ast;

  const testCases = [];

  traverse(ast, {FunctionDeclaration(path) {
    // For each function, generate test assertions and a test case
    const functionName = path.node.id.name;

    const assertions = [];
    assertions.push(`// Test Case for ${functionName}`);
    assertions.push(`test('${functionName} renders correctly', () => {`);
    
    // Include assertions for rendering
    assertions.push(`  const { getByText, getByTestId } = render(<${functionName} />);`);
    assertions.push(`  expect(getByText('Count:')).toBeInTheDocument();`);

    // Include assertions for state changes and interactions
    if (functionName === 'ComplexComponent') {
      assertions.push(`  const incrementButton = getByText('Increment');`);
      assertions.push(`  fireEvent.click(incrementButton);`);
      assertions.push(`  expect(getByText('Count: 1')).toBeInTheDocument();`);
    }

    // Your custom assertions here

    assertions.push('});'); // Close the test case

    testCases.push(assertions.join('\n'));
  },
  VariableDeclarator(path) {
    // Include assertions for variable declarations
    const variableName = path.node.id.name;
    testCases.push(`// Test Case for ${variableName}`);
    testCases.push(`test('${variableName} is initialized correctly', () => {`);
    testCases.push(`  const ${variableName} = yourMockFunction();`);
    testCases.push(`  // Add assertions for ${variableName}`);
    testCases.push(`  expect(/* Your assertion here */).toBeTruthy();`);
    testCases.push('});');
  },
  JSXElement(path) {
    // Include assertions for JSX elements
    const elementName = path.node.openingElement.name.name;
    testCases.push(`// Test Case for ${elementName}`);
    testCases.push(`test('${elementName} is present', () => {`);
    testCases.push(`  const { getByTestId } = render(/* Your component */);`);
    testCases.push(`  expect(getByTestId('${elementName.toLowerCase()}')).toBeInTheDocument();`);
    testCases.push('});');
  },
  CallExpression(path) {
    // Include assertions for function calls
    const functionName = path.node.callee.name;
    testCases.push(`// Test Case for ${functionName}`);
    testCases.push(`test('${functionName} returns a defined value', () => {`);
    testCases.push(`  const result = ${functionName}();`);
    testCases.push(`  expect(result).toBeDefined();`);
    testCases.push('});');
  },
  ConditionalExpression(path) {
    // Include assertions for conditional expressions
    testCases.push(`// Test Case for Conditional Expression`);
    testCases.push(`test('Conditional expression evaluates correctly', () => {`);
    testCases.push(`  const condition = true;`);
    testCases.push(`  const result = condition ? yourMockFunction() : null;`);
    testCases.push(`  expect(result).toBeNull();`);
    testCases.push('});');
  },
  AssignmentExpression(path) {
    // Include assertions for assignment expressions
    const variableName = path.node.left.name;
    testCases.push(`// Test Case for Assignment Expression`);
    testCases.push(`test('${variableName} is updated correctly', () => {`);
    testCases.push(`  let ${variableName} = initialValue;`);
    testCases.push(`  ${variableName} = updatedValue;`);
    testCases.push(`  expect(${variableName}).toEqual(updatedValue);`);
    testCases.push('});');
  },
  BinaryExpression(path) {
    // Include assertions for binary expressions
    testCases.push(`// Test Case for Binary Expression`);
    testCases.push(`test('Binary expression evaluates correctly', () => {`);
    testCases.push(`  const result = 2 + 3;`);
    testCases.push(`  expect(result).toEqual(5);`);
    testCases.push('});');
  },
  MemberExpression(path) {
    // Include assertions for member expressions
    const propertyName = path.node.property.name;
    testCases.push(`// Test Case for Member Expression`);
    testCases.push(`test('${propertyName} is accessed correctly', () => {`);
    testCases.push(`  const obj = { ${propertyName}: 'value' };`);
    testCases.push(`  expect(obj.${propertyName}).toEqual('value');`);
    testCases.push('});');
  },
  ArrayExpression(path) {
    // Include assertions for array expressions
    testCases.push(`// Test Case for Array Expression`);
    testCases.push(`test('Array is created correctly', () => {`);
    testCases.push(`  const arr = [1, 2, 3];`);
    testCases.push(`  expect(arr).toHaveLength(3);`);
    testCases.push('});');
  },
  ObjectExpression(path) {
    // Include assertions for object expressions
    testCases.push(`// Test Case for Object Expression`);
    testCases.push(`test('Object is created correctly', () => {`);
    testCases.push(`  const obj = { key: 'value' };`);
    testCases.push(`  expect(obj).toHaveProperty('key', 'value');`);
    testCases.push('});');
  },
  LogicalExpression(path) {
    // Include assertions for logical expressions
    testCases.push(`// Test Case for Logical Expression`);
    testCases.push(`test('Logical expression evaluates correctly', () => {`);
    testCases.push(`  const result = true && false;`);
    testCases.push(`  expect(result).toBeFalsy();`);
    testCases.push('});');
  },
  UnaryExpression(path) {
    // Include assertions for unary expressions
    testCases.push(`// Test Case for Unary Expression`);
    testCases.push(`test('Unary expression evaluates correctly', () => {`);
    testCases.push(`  const result = !true;`);
    testCases.push(`  expect(result).toBeFalsy();`);
    testCases.push('});');
  },
    
  });

  return testCases.join('\n\n');
}

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
