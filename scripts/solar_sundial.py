import matplotlib.pyplot as plt
from datetime import timedelta
import solarpy as sp
import pandas as pd
import numpy as np

# Script utilizado para cálculo de geometría solar anual para la ubicación del Reloj Solar Analemático


def lng_to360(lng_input):
    if lng_input < 0:
        return abs(lng_input)
    elif 0 < lng_input < 180:
        return lng_input + 180


def standard2solar_time_modified(date, lng, lng_std):
    """
    solarpy.standar2solar_time() modified function from solarpy
    Solar time for a particular longitude, date and *standard* time.

    Parameters
    ----------
    date : datetime object
        standard (or local) time
    lng : float
        longitude
    lng_std: float
        standard longitude

    Returns
    -------
    solar time : datetime object
        solar time
    """
    sp.check_long(lng)

    # standard time
    t_std = date
    lng_360 = lng_to360(lng)
    lng_std_360 = lng_to360(lng_std)

    # displacement from standard meridian for that longitude
    delta_std_meridian = timedelta(minutes=(4 * (lng_std_360 - lng_360)))

    # eq. of time for that day
    e_param = timedelta(minutes=sp.eq_time(date))
    t_solar = t_std + delta_std_meridian + e_param
    return t_solar


def time_height(min_height, latitude_input, declination):
    height_output = - min_height * np.tan(latitude_input - declination)
    return height_output


# Parámetros del sitio
latitude = -32.883
longitude = -68.833
longitude_std = -45
user_height = 1.4


year_2023 = pd.date_range("2023-01-01 00:00", "2023-12-31 23:59", freq="min")
# Declinación solar
declination_list = [np.rad2deg(sp.declination(date)) for date in year_2023]
# Día Juliano
julian_day = [sp.day_of_the_year(date) for date in year_2023]
# Hora solar
solar_time = pd.Series([standard2solar_time_modified(date, longitude, longitude_std) for date in year_2023])
# Ángulo horario
hour_angle = pd.Series([np.rad2deg(sp.hour_angle(date)) for date in solar_time])
# Altura de la sombra
shadow_height = [time_height(user_height, np.deg2rad(latitude), decl) for decl in np.deg2rad(declination_list)]
# Ángulo cenital
theta_z = [sp.theta_z(date, latitude) for date in year_2023]

# Cálculos dimensiones de la elipse
ellipse_max_radius = 2
ellipse_min_radius = np.abs(ellipse_max_radius * np.sin(np.deg2rad(latitude)))
ellipse_focus = np.sqrt(ellipse_max_radius**2 - ellipse_min_radius**2)
t = np.linspace(-120, 120, 17)
x = ellipse_max_radius * np.sin(np.deg2rad(t))
y = ellipse_max_radius * np.sin(np.deg2rad(latitude)) * np.cos(np.deg2rad(t))
x = x.tolist()
y = y.tolist()
# Marcas en regla central
z = pd.Series(ellipse_max_radius * np.tan(np.deg2rad(declination_list)) * np.cos(np.deg2rad(latitude)))

# Estructuración de datos en DataFrame (minuto a minuto)
df = pd.DataFrame({"julian_day": julian_day, "datetime": year_2023, "declination": declination_list,
                   "solar_time": solar_time.dt.time, "hour_angle": hour_angle, "shadow_height": shadow_height, "z": z})
# Simplificación de la estructura minutal a diaria
df_diario = df[df["hour_angle"] == 0].reset_index(drop=True)
z_diario = df_diario["z"]

print(f"Valor máximo de declinación: {max(declination_list)}")
print(f"Valor mínimo de declinación: {min(declination_list)}")

# ---------- Dibujo reloj
hours_plot = np.flip(range(4, 21))
y_plot = [-element for element in y]
# Dibujo puntos de la elipse
plt.plot(x, y_plot, "k.", markersize=35)
# Texto en los puntos de la elipse
for i, e in enumerate(x):
    plt.text(e, y_plot[i] + 0.08, hours_plot[i], horizontalalignment="center", size="xx-large")
# Dibujo puntos regla central
plt.plot([0, 0, 0, 0, 0, 0, 0], [-z_diario[i] for i in [173, 142, 112, 81, 53, 22, 356]], color="#2D97D9", marker=".", markersize=35)
# Dibujo regla central
plt.vlines(0, ymin=min(z_diario), ymax=max(z_diario), linestyles="dotted", colors="#2D97D9", linewidth=6)
# Texto en la regla central
plt.text(0, -z_diario[173], "21 JUN   ", ha="right", va="center", size="xx-large")
plt.text(0, -z_diario[142], "21 MAY   ", ha="right", va="center", size="xx-large")
plt.text(0, -z_diario[142], "   24 JUL", ha="left", va="center", size="xx-large")
plt.text(0, -z_diario[112], "21 ABR   ", ha="right", va="center", size="xx-large")
plt.text(0, -z_diario[112], "   23 AGO", ha="left", va="center", size="xx-large")
plt.text(0, -z_diario[81], "21 MAR   ", ha="right", va="center", size="xx-large")
plt.text(0, -z_diario[81], "   24 SEP", ha="left", va="center", size="xx-large")
plt.text(0, -z_diario[53], "21 FEB   ", ha="right", va="center", size="xx-large")
plt.text(0, -z_diario[53], "   22 OCT", ha="left", va="center", size="xx-large")
plt.text(0, -z_diario[22], "21 ENE   ", ha="right", va="center", size="xx-large")
plt.text(0, -z_diario[22], "   22 NOV", ha="left", va="center", size="xx-large")
plt.text(0, -z_diario[356], "   21 DIC", ha="left", va="center", size="xx-large")
# Dibujo 29 de abril
plt.arrow(-0.5, -z_diario[120], 0.4, 0, width=0.02, color="red")
plt.text(-0.51, -z_diario[120], "29 ABR", ha="right", va="center", size="xx-large", color="red")
plt.gca().set_aspect("equal")
plt.axis("off")
plt.show()
