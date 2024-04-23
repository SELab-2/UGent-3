export default {
  preset: 'vite-jest',
  testMatch: [
    '**/tests/jest/**/*.ts?(x)'
  ],
  testEnvironment: 'jest-environment-jsdom'
};