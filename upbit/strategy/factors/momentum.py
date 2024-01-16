import pandas as pd
import numpy as np

from ...modules import (
    annualize_scaler, convert_freq,
    rebal_dates, price_on_rebal
)

class MomentumFactor:
    """Momentum 전략을 관리할 클래스
    Returns:
        pd.DataFrame -> 거래 시그널을 알려주는 df
    """
    
    def __init__(self, price_df: pd.DataFrame,
                 freq: str='M', lookback_window: int=1,
                 n_sel: int=20, long_only: bool=True):
        """초기화 함수
        Args:
            rebal_price (pd.DataFrame): 
                - DataFrame -> 일별 종가 데이터프레임
            lookback_window (int):
                - int -> 모멘텀(추세)를 확인할 기간 설정
            n_sel (int):
                - int -> 몇 개의 금융상품을 고를지 결정
            long_only (bool, optional): 
                - bool -> 매수만 가능한지 아님 공매도까지 가능한지 결정. Defaults to True.
        """
        self.freq = convert_freq(freq)
        self.lookback_window = lookback_window * annualize_scaler(self.freq)
        self.rebal_dates_list = rebal_dates(price_df, 
                                            period=self.freq)
        
        self.rets = price_df.loc[self.rebal_dates_list, :].pct_change(self.lookback_window).dropna()
        self.n_sel = n_sel
        self.long_only = long_only

    # 절대 모멘텀 시그널 계산 함수
    def absolute_momentum(self) -> pd.DataFrame:
        """absolute_momentum
        Args:
            long_only (bool, optional): 
                - bool -> 매수만 가능한지 결정. Defaults to True.
        Returns:
            pd.DataFrame -> 투자 시그널 정보를 담고있는 df
        """

        returns = self.rets

        # 롱 시그널
        long_signal = (returns > 0) * 1

        # 숏 시그널
        short_signal = (returns < 0) * -1

        # 토탈 시그널
        if self.long_only == True:
            signal = long_signal

        else:
            signal = long_signal + short_signal
        
        return signal#.dropna(inplace=True)
    
    # 상대 모멘텀 시그널 계산 함수
    def relative_momentum(self) -> pd.DataFrame:
        """relative_momentum
        Args:
            long_only (bool, optional): 
                - bool -> 매수만 가능한지 결정. Defaults to True.
        Returns:
            pd.DataFrame -> 투자 시그널 정보를 담고있는 df
        """

        # 수익률
        returns = self.rets

        # 자산 개수 설정
        n_sel = self.n_sel

        # 수익률 순위화
        rank = returns.rank(axis=1, ascending=False)

        # 롱 시그널
        long_signal = (rank <= n_sel) * 1

        # 숏 시그널
        short_signal = (rank >= len(rank.columns) - n_sel + 1) * -1

        # 토탈 시그널
        if self.long_only == True:
            signal = long_signal

        else:
            signal = long_signal + short_signal

        return signal#.dropna(inplace=True)
    
    # 듀얼 모멘텀 시그널 계산 함수
    def dual_momentum(self) -> pd.DataFrame:
        """dual_momentum
        Args:
            long_only (bool, optional): 
                - bool -> 매수만 가능한지 결정. Defaults to True.
        Returns:
            pd.DataFrame -> 투자 시그널 정보를 담고있는 df
        """

        # 절대 모멘텀 시그널
        abs_signal = self.absolute_momentum()

        # 상대 모멘텀 시그널
        rel_signal = self.relative_momentum()

        # 듀얼 모멘텀 시그널
        signal = (abs_signal == rel_signal) * abs_signal

        # 절대 모멘텀과 상대 모멘텀의 시그널을 받을 때 이미 signal.iloc[self.lookback_window:,] 반영되어 있음
        return signal

    def signal(self):
        return self.dual_momentum()