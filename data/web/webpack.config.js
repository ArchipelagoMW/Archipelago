const path = require('path');

module.exports = {
  mode: 'production',
  watch: false,
  resolve: {
    fallback: {
      crypto: require.resolve('crypto-browserify'),
      buffer: require.resolve('buffer/'),
      stream: require.resolve('stream-browserify'),
    },
  },
  entry: {
    index: './src/js/index.js',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx|es6)$/,
        loader: 'babel-loader',
        options: {
          compact: true,
          minified: true,
        },
      },
      {
        test: /\.((css)|(s[a|c]ss))$/,
        use: [
          { loader: 'style-loader' },
          { loader: 'css-loader' },
          { loader: 'sass-loader' },
        ],
      },
      {
        test: /\.(otf)$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'fonts/',
              publicPath: 'assets/fonts/',
            },
          },
        ],
      },
    ],
  },
  output: {
    path: `${path.resolve(__dirname)}/public/assets`,
    publicPath: '/',
    filename: '[name].bundle.js',
  },
};
