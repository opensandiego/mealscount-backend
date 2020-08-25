const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = { 
  entry: './src/index.js', 
  mode: 'development',
  output: { 
    path: path.resolve(__dirname,'dist'), 
    filename: 'static/index_bundle.js?' + process.env.SOURCE_VERSION,
  }, 
  module: {
    rules: [
        {
            test: /\.css$/,
            use: [
                'style-loader',
                'css-loader'
            ]
        },
        {
            test: /\.(png|svg|jpg|jpeg|gif|pdf)$/,
            use: [{
                loader: 'file-loader',
                options: {
                  outputPath: 'static'
                }
            }]
        },
        {
          test: /\.(scss)$/,
          use: [{
            loader: 'style-loader', // inject CSS to page
          }, {
            loader: 'css-loader', // translates CSS into CommonJS modules
          }, {
            loader: 'postcss-loader', // Run postcss actions
            options: {
              plugins: function () { // postcss plugins, can be exported to postcss.config.js
                return [
                  require('autoprefixer')
                ];
              }
            }
          }, {
            loader: 'sass-loader' // compiles Sass to CSS
          }]
        },
        {
          test: /\.vue$/,
          loader: 'vue-loader'
        },
    ],
  },
  plugins: [
    new VueLoaderPlugin(),
    new HtmlWebpackPlugin({
      filename: 'index.html',
      title: 'Output Management',
      template: 'src/index.html',
      inject: true,
    }),
  ],
  devServer: {
    contentBase: path.join(__dirname, 'dist'),
    historyApiFallback: true,
    hot: true,
    proxy: {
      '/api': { target:'https://www.mealscount.com/', changeOrigin: true  },
      '/static': { target:'https://www.mealscount.com/', changeOrigin: true }
    }
  }
}
