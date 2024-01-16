import pandas as pd

def moving_average(price: pd.DataFrame, window: int) -> pd.DataFrame:
    """이동평균선 계산 함수
    Args:
        price (pd.DataFrame): 
            - DataFrame -> 일별 종가 데이터프레임
        window (int): 
            - int -> 이동평균선의 기간
    Returns:
        pd.DataFrame: 이동평균선 데이터프레임
    """
    ma = price.rolling(window).mean().dropna()
    return ma

def bollinger_band(price: pd.DataFrame,
                   window: int=20,
                   upper: bool=True) -> pd.DataFrame:
    """볼린저 밴드 계산 함수
    Args:
        price (pd.DataFrame): 
            - DataFrame -> 일별 종가 데이터프레임
        window (int, optional): 
            - int -> 이동평균선의 기간. Defaults to 20.
        upper (bool, optional): 
            - bool -> 상단 볼린저 밴드 계산 여부. Defaults to True.
    Returns:
        pd.DataFrame: 볼린저 밴드 데이터프레임
    """
    ma = moving_average(price, window)
    std = price.rolling(window).std().dropna()
    
    bb = pd.DataFrame()
    bb['mid'] = ma
    bb['upper'] = ma + (std * 2)
    bb['lower'] = ma - (std * 2)
    
    return bb

def ichimoku(price: pd.DataFrame,
             transfer_window: int=9,
             standard_window: int=26,
             signal_window: int=52) -> pd.DataFrame:
    """일목균형표 계산 함수
    Args:
        price (pd.DataFrame):
            - DataFrame -> 일별 종가 데이터프레임
        transfer_window (int, optional):
            - int -> 전환선의 기간. Defaults to 9.
        standard_window (int, optional):
            - int -> 기준선의 기간. Defaults to 26.
        signal_window (int, optional):
            - int -> 후행스팬의 기간. Defaults to 52.
    
    Returns:
        pd.DataFrame: 일목균형표 데이터프레임"""
    ichimoku = pd.DataFrame()
    ichimoku['tenkan'] = (price['high'].rolling(transfer_window).max() + price['low'].rolling(transfer_window).min()) / 2
    ichimoku['kijun'] = (price['high'].rolling(standard_window).max() + price['low'].rolling(standard_window).min()) / 2
    ichimoku['senkou_a'] = ((ichimoku['tenkan'] + ichimoku['kijun']) / 2).shift(transfer_window)
    ichimoku['senkou_b'] = ((price['high'].rolling(signal_window).max() + price['low'].rolling(signal_window).min()) / 2).shift(transfer_window)
    ichimoku['chikou'] = price['close'].shift(-transfer_window)
    
    return ichimoku

def parabolic_sar(price: pd.DataFrame,
                    af: float=0.02,
                    max_af: float=0.2) -> pd.DataFrame:
    """파라볼릭 SAR 계산 함수
    Args:
        price (pd.DataFrame):
            - DataFrame -> 일별 종가 데이터프레임
        af (float, optional):
            - float -> 가속도 계수. Defaults to 0.02.
        max_af (float, optional):
            - float -> 최대 가속도 계수. Defaults to 0.2.
            
    Returns:
        pd.DataFrame: 파라볼릭 SAR 데이터프레임
    """
    sar = pd.DataFrame()
    sar['trend'] = price['close'].diff()
    sar['trend'] = sar['trend'].apply(lambda x: 1 if x > 0 else -1)
    sar['ep'] = price['high'].rolling(2).max() if sar['trend'].iloc[0] == 1 else price['low'].rolling(2).min()
    sar['sar'] = price['close'].shift(1)
    sar['af'] = af
    
    for i in range(2, len(sar)):
        if sar['trend'].iloc[i] == sar['trend'].iloc[i-1]:
            sar['ep'].iloc[i] = sar['ep'].iloc[i-1]
            sar['sar'].iloc[i] = sar['sar'].iloc[i-1] + sar['af'].iloc[i] * (sar['ep'].iloc[i] - sar['sar'].iloc[i-1])
            sar['af'].iloc[i] = min(sar['af'].iloc[i-1] + af, max_af)
        
        else:
            sar['ep'].iloc[i] = price['high'].iloc[i] if sar['trend'].iloc[i] == 1 else price['low'].iloc[i]
            sar['sar'].iloc[i] = sar['ep'].iloc[i-1]
            sar['af'].iloc[i] = af
        
    return sar['sar']

def price_channel(price: pd.DataFrame,
                  window: int=20) -> pd.DataFrame:
    """가격 채널 계산 함수
    Args:
        price (pd.DataFrame): 
            - DataFrame -> 일별 종가 데이터프레임
    Returns:
        pd.DataFrame: 가격 채널 데이터프레임
    """
    pc = pd.DataFrame()
    pc['upper'] = price.rolling(window).max()
    pc['lower'] = price.rolling(window).min()
    pc['mid'] = (pc['upper'] + pc['lower']) / 2
    
    return pc

def cross_analysis(price: pd.DataFrame,
                   short_window: int,
                   long_window: int,
                   cross_window: int):
    cross = cross_window + 1
    
    short_ma = moving_average(price, short_window)
    long_ma = moving_average(price, long_window)
    
    result = {}
    for stock in price.columns:
        if short_ma[stock].iloc[-1] > long_ma[stock].iloc[-1]:
            if short_ma[stock].iloc[-cross] < long_ma[stock].iloc[-cross]:
                result[stock] = 'golden_cross'
            else:
                result[stock] = 'holding'
        else:
            if short_ma[stock].iloc[-cross] > long_ma[stock].iloc[-cross]:
                result[stock] = 'dead_cross'
            else:
                result[stock] = 'holding'
                
    return result

def rsi(price: pd.DataFrame,
        window: int=20) -> pd.DataFrame:
    """RSI 계산 함수
    Args:
        price (pd.DataFrame): 
            - DataFrame -> 일별 종가 데이터프레임
        window (int, optional): 
            - int -> RSI의 기간. Defaults to 20.
    Returns:
        pd.DataFrame: RSI 데이터프레임
    """
    delta = price.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    
    roll_up = up.ewm(window).mean()
    roll_down = down.abs().ewm(window).mean()
    
    rsi = 100.0 - (100.0 / (1.0 + (roll_up / roll_down))) if roll_down != 0 else 100.0
    
    return rsi

def momentum(price: pd.DataFrame,
             window: int=20) -> pd.DataFrame:
    """모멘텀 계산 함수
    Args:
        price (pd.DataFrame): 
            - DataFrame -> 일별 종가 데이터프레임
        window (int, optional): 
            - int -> 모멘텀의 기간. Defaults to 20.
    Returns:
        pd.DataFrame: 모멘텀 데이터프레임
    """
    momentum = price / price.shift(window) - 1
    return momentum

def volatility(price: pd.DataFrame,
               window: int=20) -> pd.DataFrame:
    """변동성 계산 함수
    Args:
        price (pd.DataFrame): 
            - DataFrame -> 일별 종가 데이터프레임
        window (int, optional): 
            - int -> 변동성의 기간. Defaults to 20.
    Returns:
        pd.DataFrame: 변동성 데이터프레임
    """
    vol = price.pct_change().rolling(window).std().dropna()
    return vol

def cci(price: pd.DataFrame,
        window: int=20) -> pd.DataFrame:
    """CCI 계산 함수,
-100 이하면 과매도, +100 이상이면 과매수
단, 후행성 지표이므로 신호가 나타난 후에는 반드시 확인 필요
0선을 추세판단 기준으로 사용하기도 함.

    Args:
        price (pd.DataFrame): 
            - DataFrame -> 종목별 캔들 데이터프레임 (open, high, low, trade)
ex)
date | open | high | low | trade
---- | ---- | ---- | --- | -----
2023-10-11 | 111 | 124 | 100 | 120
2023-10-12 | 120 | 130 | 110 | 125
2023-10-13 | 125 | 130 | 120 | 130
2023-10-14 | 130 | 140 | 120 | 135

        window (int, optional): 
            - int -> CCI의 기간. Defaults to 20.
    Returns:
        pd.DataFrame: CCI 데이터프레임
    """
    tp = (price['high'] + price['low'] + price['close']) / 3
    cci = (tp - tp.rolling(window).mean()).dropna() / (0.015 * tp.rolling(window).std()).dropna()
    return cci

def atr(price: pd.DataFrame,
        window: int=20) -> pd.DataFrame:
    """ATR 계산 함수
    Args:
        price (pd.DataFrame): 
            - DataFrame -> 종목별 캔들 데이터프레임 (open, high, low, trade)
ex)
date | open | high | low | trade
---- | ---- | ---- | --- | -----
2023-10-11 | 111 | 124 | 100 | 120
2023-10-12 | 120 | 130 | 110 | 125
2023-10-13 | 125 | 130 | 120 | 130
2023-10-14 | 130 | 140 | 120 | 135

        window (int, optional): 
            - int -> ATR의 기간. Defaults to 20.
    Returns:
        pd.DataFrame: ATR 데이터프레임
    """
    tr = pd.DataFrame()
    tr['tr1'] = price['high'] - price['low']
    tr['tr2'] = abs(price['high'] - price['trade'].shift())
    tr['tr3'] = abs(price['low'] - price['trade'].shift())
    tr['tr'] = tr.max(axis=1)
    atr = tr['tr'].rolling(window).mean()
    return atr

def stochastic_fast(price: pd.DataFrame,
                    K_window: int=15,
                    D_window: int=0) -> pd.DataFrame:
    """Stochastic Fast 계산 함수
    Args:
        price (pd.DataFrame): 
            - DataFrame -> 종목별 캔들 데이터프레임 (open, high, low, trade)
ex)
date | open | high | low | trade
---- | ---- | ---- | --- | -----
2023-10-11 | 111 | 124 | 100 | 120
2023-10-12 | 120 | 130 | 110 | 125
2023-10-13 | 125 | 130 | 120 | 130
2023-10-14 | 130 | 140 | 120 | 135

        K_window (int, optional):
            - int -> Fast K의 기간. Defaults to 15.
        D_window (int, optional):
            - int -> Fast D의 기간. Defaults to 0.
    
    Returns:
        pd.DataFrame: Stochastic Fast 데이터프레임. D_window가 0이면 Fast K, 아니면 Fast D 
    """
    fast_k = (price['trade'] - price['low'].rolling(K_window).min()) / (price['high'].rolling(K_window).max() - price['low'].rolling(K_window).min())
    
    if D_window == 0:
        return fast_k
    
    elif D_window > 0:
        return fast_k.rolling(D_window).mean()
    
    else:
        raise ValueError("window must be positive integer")

def macd(price: pd.DataFrame,
         short_window: int=12,
         long_window: int=26,
         signal_window: int=9) -> pd.DataFrame:
    """MACD 계산 함수
    Args:
        price (pd.DataFrame): 
            - DataFrame -> 종목별 캔들 데이터프레임 (open, high, low, trade)
            
ex)

date | open | high | low | trade
---- | ---- | ---- | --- | -----
2023-10-11 | 111 | 124 | 100 | 120
2023-10-12 | 120 | 130 | 110 | 125

        short_window (int, optional):
            - int -> 단기 이동평균선의 기간. Defaults to 12.
            
        long_window (int, optional):
            - int -> 장기 이동평균선의 기간. Defaults to 26.
        
        signal_window (int, optional):
            - int -> 시그널의 기간. Defaults to 9.
            
    Returns:
        pd.DataFrame: MACD 데이터프레임
    """
    macd = moving_average(price, short_window) - moving_average(price, long_window)
    signal = moving_average(macd, signal_window)
    
    return macd, signal