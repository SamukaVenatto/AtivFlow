module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/setupTests.js'],
  moduleNameMapper: {
    '\\.(css|less|sass|scss)$': 'identity-obj-proxy',
    '^.+\\\.svg$': 'jest-svg-transformer',
    '^.+\\\.png$': '<rootDir>/fileTransformer.js',
  },
  transform: {
    '^.+\\\.jsx?$': 'babel-jest',
  },
};

