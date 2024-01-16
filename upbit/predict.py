import pyupbit
from prophet import Prophet
from datetime import datetime

class predict:
    def __init__(self, ticker="KRW-BTC", interval="minute60", count=200, period=24, freq='H'):
        self.market = ticker
        self.interval = interval
        self.count = count
        
        df = pyupbit.get_ohlcv(ticker=ticker, interval=interval, count=count)
        df = df.reset_index()
        df['ds'] = df['index']
        df['price'] = df['close']
        self.data = df[['ds','price']]

        self.model = Prophet()
        self.model.fit(self.data)
        self.future = self.model.make_future_dataframe(periods=period, freq=freq)
        self.forecast = self.model.predict(self.future)

    def plot(self):
        self.model.plot(self.forecast).savefig(
            f"{self.market}model_{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
        )
        self.model.plot_components(self.forecast).savefig(
            f"{self.market}model_components_{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
        )

    def is_upward(self) -> bool:
        return 

    def backtest(self):
        pass


if __name__ == '__main__':
    df = pyupbit.get_ohlcv(count=10)
    df