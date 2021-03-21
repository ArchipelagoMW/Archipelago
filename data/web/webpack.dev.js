const path = require('path');

module.exports = {
  mode: 'development',
  watch: true,
  resolve: {
    fallback: {
      crypto: require.resolve('crypto-browserify'),
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
          compact: false,
          minified: false,
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
