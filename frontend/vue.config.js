module.exports = {
  "devServer": {
    "proxy": {
      "^/": {
        "target": "http://127.0.0.1:8000/",
        "ws": false
      }
    }
  },
  "outputDir": "./dist/",
  "assetsDir": "static",
  "transpileDependencies": [
    "vuetify"
  ]
}