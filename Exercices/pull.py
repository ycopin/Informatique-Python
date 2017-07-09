#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as N


def pull(x, dx):
    """
    Compute the pull from x, dx.

    * Input data: x = [x_i], error dx = [s_i] Optimal
    * (variance-weighted) mean: E = sum(x_i/s_i²)/sum(1/s_i²) Variance
    * on weighted mean: var(E) = 1/sum(1/s_i²) Pull: p_i = (x_i -
    * E_i)/sqrt(var(E_i) + s_i²) where E_i and var(E_i) are computed
    * without point i.

    If errors s_i are correct, the pull distribution is centered on 0
    with standard deviation of 1.
    """

    assert x.ndim == dx.ndim == 1, "pull works on 1D-arrays only."
    assert len(x) == len(dx), "dx should be the same length as x."

    n = len(x)

    i = N.resize(N.arange(n), n * n)  # 0,...,n-1,0,...n-1,..., n times (n²,)
    i[::n + 1] = -1                  # Mark successively 0,1,2,...,n-1
    # Remove marked indices & reshape (n,n-1)
    j = i[i >= 0].reshape((n, n - 1))

    v = dx ** 2                      # Variance
    w = 1 / v                        # Variance (optimal) weighting

    Ei = N.average(x[j], weights=w[j], axis=1)  # Weighted mean (n,)
    vEi = 1 / N.sum(w[j], axis=1)                # Variance of mean (n,)

    p = (x - Ei) / N.sqrt(vEi + v)               # Pull (n,)

    return p

if __name__ == '__main__':

    import matplotlib.pyplot as P
    import scipy.stats as SS

    n = 1000
    mu = 1.
    sig = 2.

    # Normally distributed random sample of size n, with mean=mu and std=sig
    x = N.random.normal(loc=mu, scale=sig, size=n)
    dx = N.full_like(x, sig)              # Formal (true) errors

    p = pull(x, dx)                       # Pull computation

    m, s = p.mean(), p.std(ddof=1)
    print "Pull ({} entries): mean={:.2f}, std={:.2f}".format(n, m, s)

    fig, ax = P.subplots()
    _, bins, _ = ax.hist(p, bins='auto', normed=True,
                         histtype='stepfilled',
                         label=u"#={}, µ={:.3f}, σ={:.3f}".format(n, m, s))
    y = N.linspace(-3, 3)
    ax.plot(y, SS.norm.pdf(y), label=ur"$\mathcal{N}$(µ=0, σ²=1)")
    ax.set(title='Pull distribution', xlabel='Pull')
    ax.legend(loc='upper left')

    P.show()
