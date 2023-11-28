import pandas as pd
import solarpy as sp
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import locale


year = pd.date_range("2023-01-01 00:00", "2023-12-31 23:59", freq="d")
declination = [np.rad2deg(sp.declination(date)) for date in year]
eot = [sp.eq_time(date) for date in year]
time_dif = [-(4*(45 - 68.83) + E) for E in eot]

# Gráfico de la ecuación del tiempo
fig, ax = plt.subplots(1, 1)
ax.plot(np.linspace(1, 365, len(time_dif)), eot, linewidth=5, color="#2D97D9")

ax.set_xlabel("Fecha", fontsize=30)
ax.set_ylabel("Minutos", fontsize=30)

# Set the locator
locale.setlocale(locale.LC_ALL, 'esp')
locator = mdates.MonthLocator()  # every month
# Specify the format - %b gives us Jan, Feb...
fmt = mdates.DateFormatter('%d/%m')
X = plt.gca().xaxis
X.set_major_locator(locator)
# Specify formatter
X.set_major_formatter(fmt)
ax.tick_params(axis="x", labelsize=20)
ax.tick_params(axis="y", labelsize=20)
ax.grid()
fig.autofmt_xdate()
plt.legend(["Ecuación del tiempo"], fontsize=20)
plt.show()


# Gráfico del analema
# fig, ax = plt.subplots()
# x_major_ticks = np.arange(min(eot), max(eot), 10)
# x_minor_ticks = np.arange(min(eot), max(eot), 1)
# y_minor_ticks = np.arange(min(declination), max(declination), 1)
# ax.set_xticks(x_minor_ticks, minor=True)
# ax.set_yticks(y_minor_ticks, minor=True)
# plt.plot(eot, declination, color="black")
# plt.title("Analema")
# plt.xlabel("Equación del tiempo (E)")
# plt.ylabel("Declinación (°)")
# plt.grid()
# ax.set_aspect("equal")
# plt.show()
