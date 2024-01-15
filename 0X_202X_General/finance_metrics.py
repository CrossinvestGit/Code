import datetime

import numpy as np
from tabulate import tabulate


def calculate_drawdowns(timeseries, n):
    """
    Calculate the top n drawdowns of a time series.

    Parameters:
    timeseries (array-like): Time series data.
    n (int): Number of top drawdowns to calculate.

    Returns:
    str: Table of top n drawdowns.
    """
    drawdowns = []
    peak = timeseries[0]
    peak_date = datetime.datetime.now()
    start_date = datetime.datetime.now()
    end_date = datetime.datetime.now()
    duration = 0

    for i in range(1, len(timeseries)):
        if timeseries[i] > peak:
            peak = timeseries[i]
            peak_date = datetime.datetime.now()

        drawdown = (peak - timeseries[i]) / peak
        drawdowns.append(
            {
                "beginning_of_drawdown": start_date,
                "end_of_drawdown": end_date,
                "severity_of_drawdown": drawdown * 100,
                "duration_of_drawdown": duration,
            }
        )

        if timeseries[i] < peak:
            if start_date == datetime.datetime.now():
                start_date = datetime.datetime.now()
            end_date = datetime.datetime.now()
            duration += 1

    top_n_drawdowns = sorted(drawdowns, key=lambda x: x["severity_of_drawdown"])[:n]
    table = tabulate(top_n_drawdowns, headers="keys", tablefmt="grid")
    return table


def caculate_rolling_volatility(timeseries, n):
    """
    Calculate the rolling volatility of a time series.

    Parameters:
    timeseries (array-like): Time series data.
    n (int): Number of top drawdowns to calculate.

    Returns:
    str: Table of top n drawdowns.
    """
    rolling_volatility = []
    for i in range(0, len(timeseries)):
        if i > n:
            rolling_volatility.append(np.std(timeseries[i - n : i]))

    return rolling_volatility


def calculate_rolling_tracking_error(portfolio_returns, benchmark_returns, n):
    """
    Calculate the rolling tracking error of a portfolio.

    Parameters:
    portfolio_returns (array-like): Portfolio returns.
    benchmark_returns (array-like): Benchmark returns.
    n (int): Number of top drawdowns to calculate.

    Returns:
    str: Table of top n drawdowns.
    """
    rolling_tracking_error = []
    for i in range(0, len(portfolio_returns)):
        if i > n:
            rolling_tracking_error.append(
                np.std(portfolio_returns[i - n : i] - benchmark_returns[i - n : i])
            )

    return rolling_tracking_error


def calculate_rolling_beta(portfolio_returns, benchmark_returns, n):
    """
    Calculate the rolling beta of a portfolio.

    Parameters:
    portfolio_returns (array-like): Portfolio returns.
    benchmark_returns (array-like): Benchmark returns.
    n (int): Number of top drawdowns to calculate.

    Returns:
    str: Table of top n drawdowns.
    """
    rolling_beta = []
    for i in range(0, len(portfolio_returns)):
        if i > n:
            rolling_beta.append(
                np.cov(portfolio_returns[i - n : i], benchmark_returns[i - n : i])[0][1]
                / np.var(benchmark_returns[i - n : i])
            )

    return rolling_beta


def calculate_rolling_sharpe_ratio(portfolio_returns, n):
    """
    Calculate the rolling sharpe ratio of a portfolio.

    Parameters:
    portfolio_returns (array-like): Portfolio returns.
    n (int): Number of top drawdowns to calculate.

    Returns:
    str: Table of top n drawdowns.
    """
    rolling_sharpe_ratio = []
    for i in range(0, len(portfolio_returns)):
        if i > n:
            rolling_sharpe_ratio.append(
                np.mean(portfolio_returns[i - n : i])
                / np.std(portfolio_returns[i - n : i])
            )

    return rolling_sharpe_ratio


def calculate_rolling_sortino_ratio(portfolio_returns, n):
    """
    Calculate the rolling sortino ratio of a portfolio.

    Parameters:
    portfolio_returns (array-like): Portfolio returns.
    n (int): Number of top drawdowns to calculate.

    Returns:
    str: Table of top n drawdowns.
    """
    rolling_sortino_ratio = []
    for i in range(0, len(portfolio_returns)):
        if i > n:
            rolling_sortino_ratio.append(
                np.mean(portfolio_returns[i - n : i])
                / np.std([x for x in portfolio_returns[i - n : i] if x < 0])
            )

    return rolling_sortino_ratio


def calculate_rolling_information_ratio(portfolio_returns, benchmark_returns, n):
    """
    Calculate the rolling information ratio of a portfolio.

    Parameters:
    portfolio_returns (array-like): Portfolio returns.
    benchmark_returns (array-like): Benchmark returns.
    n (int): Number of top drawdowns to calculate.

    Returns:
    str: Table of top n drawdowns.
    """
    rolling_information_ratio = []
    for i in range(0, len(portfolio_returns)):
        if i > n:
            rolling_information_ratio.append(
                np.mean(portfolio_returns[i - n : i] - benchmark_returns[i - n : i])
                / np.std(portfolio_returns[i - n : i] - benchmark_returns[i - n : i])
            )

    return rolling_information_ratio


def calculate_rolling_alpha(portfolio_returns, benchmark_returns, n):
    """
    Calculate the rolling alpha of a portfolio.

    Parameters:
    portfolio_returns (array-like): Portfolio returns.
    benchmark_returns (array-like): Benchmark returns.
    n (int): Number of top drawdowns to calculate.

    Returns:
    str: Table of top n drawdowns.
    """
    rolling_alpha = []
    for i in range(0, len(portfolio_returns)):
        if i > n:
            rolling_alpha.append(
                np.mean(portfolio_returns[i - n : i])
                - np.mean(benchmark_returns[i - n : i])
                * calculate_rolling_beta(portfolio_returns, benchmark_returns, n)[i - n]
            )

    return rolling_alpha
