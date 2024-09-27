const TradingView = require("../main");

const client = new TradingView.Client(); // websocket client

const chart = new client.Session.Chart(); // Chart session

chart.setMarket("BINANCE:BTCEUR", {
  // Hisse Seçimi
  timeframe: "1",
});

chart.onError((...err) => {
  // Hata kontrolü
  console.error("Chart error:", ...err);
});

chart.onSymbolLoaded(() => {
  // Hisse başarıyla yüklendi.
  console.log(`Hisse "${chart.infos.description}" başarıyla alındı !`);
});

chart.onUpdate(() => {
  // Fiyat değişiminde
  if (!chart.periods[0]) return;
  console.log(
    `[${chart.infos.description}]: ${chart.periods[0].close} ${chart.infos.currency_id}`
  );
});
