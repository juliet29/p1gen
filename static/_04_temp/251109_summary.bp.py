intds, extds = get_data_for_pressure("20251109_summer")
intds
# OUT: <xarray.Dataset> Size: 286kB
# OUT: Dimensions:    (datetimes: 8928)
# OUT: Coordinates:
# OUT:   * datetimes  (datetimes) datetime64[ns] 71kB 2017-05-01 ... 2017-08-01T23:4...
# OUT: Data variables:
# OUT:     A          (datetimes) float64 71kB 0.2709 0.2655 0.2667 ... 0.1565 0.02314
# OUT:     B          (datetimes) float64 71kB 0.1677 0.1842 0.2038 ... 0.0399 0.01617
# OUT:     C          (datetimes) float64 71kB 0.0887 0.1128 0.1178 ... 0.105 0.02409
intds.shape
# OUT: Traceback (most recent call last):
# OUT:   File [32m"<input>"[39m, line [35m[1m1[0m[39m, in [36m<module>[39m
# OUT:     intds.shape
# OUT:   File [32m"/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/studies2/p1gen/.venv/lib/python3.13/site-packages/xarray/core/common.py"[39m, line [35m[1m306[0m[39m, in [36m__getattr__[39m
# OUT:     raise AttributeError(
# OUT:         f"{type(self).__name__!r} object has no attribute {name!r}"
# OUT:     )
# OUT: [31m[1mAttributeError[0m[39m: [36m'Dataset' object has no attribute 'shape'[39m
intds.A.shape
# OUT: (8928,)
intds.datetimes
# OUT: <xarray.DataArray 'datetimes' (datetimes: 8928)> Size: 71kB
# OUT: array(['2017-05-01T00:00:00.000000000', '2017-05-01T00:15:00.000000000',
# OUT:        '2017-05-01T00:30:00.000000000', ..., '2017-08-01T23:15:00.000000000',
# OUT:        '2017-08-01T23:30:00.000000000', '2017-08-01T23:45:00.000000000'],
# OUT:       shape=(8928,), dtype='datetime64[ns]')
# OUT: Coordinates:
# OUT:   * datetimes  (datetimes) datetime64[ns] 71kB 2017-05-01 ... 2017-08-01T23:4...
intds.mean()
# OUT: <xarray.Dataset> Size: 24B
# OUT: Dimensions:  ()
# OUT: Data variables:
# OUT:     A        float64 8B 0.6826
# OUT:     B        float64 8B 0.6817
# OUT:     C        float64 8B 0.529
extds.mean()
# OUT: <xarray.Dataset> Size: 24B
# OUT: Dimensions:  ()
# OUT: Data variables:
# OUT:     A        float64 8B 5.978
# OUT:     B        float64 8B 6.026
# OUT:     C        float64 8B 6.026
import os
print(os.cwd())
# OUT: Traceback (most recent call last):
# OUT:   File [32m"<input>"[39m, line [35m[1m1[0m[39m, in [36m<module>[39m
# OUT:     print(os.cwd())
# OUT:           ^^^^^^
# OUT: [31m[1mAttributeError[0m[39m: [36mmodule 'os' has no attribute 'cwd'[39m
os.path.curdir
# OUT: '.'
os.getcwd()
# OUT: '/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/studies2/p1gen'
### 