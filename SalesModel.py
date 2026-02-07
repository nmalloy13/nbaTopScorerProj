import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
df = pd.read_csv(r"C:\Users\nmall\Desktop\HK Stuff\Intern Report 4.csv", header=None, names = ["Invoice/Credit", "Date", "Invoice Number", "Item", "Customer", "Item ID", "Quantity", "Cs/ea", "Price per", "Sales Total", "Customer Total"])
filter_out = ["Product Donations"]
# "Unprocessed Shopfiy Orders", "UPS - Website (Serious Sips - Shopify)"
df = df[~df['Customer'].isin(filter_out)]
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

totalByInvoice = index = df.pivot_table(
    index = ["Customer", "Date"],
    columns = "Item",
    values = "Quantity",
    aggfunc = "sum",
    fill_value = 0
).reset_index()
columns_to_drop = [col for col in totalByInvoice.columns if "SORRY!" in col]
totalByInvoice = totalByInvoice.drop(columns = columns_to_drop)

df3 = df.copy()
needed_rows = df3.groupby(["Customer","Date"]).tail(1)
needed_rows = needed_rows[["Customer", "Date", "Sales Total"]]

salesByDate = df.copy()
salesByDate = salesByDate.groupby(["Customer", "Date"], as_index=False)["Sales Total"].sum()

df4 = pd.merge(totalByInvoice, needed_rows, on = ["Customer","Date"])
pumpkin_columns = totalByInvoice[["Customer", "Date"] + list(totalByInvoice.filter(like = "Pumpkin").columns)]
pumpkin_columns = pumpkin_columns.drop(columns=pumpkin_columns.filter(like="shipped").columns)
pumpkin_columns['Total Pumpkin Products'] = pumpkin_columns.iloc[:, 2:].sum(axis=1)
pumpkin_columns = pumpkin_columns[["Customer", "Total Pumpkin Products"]]
shop_to_state = {
    "'feine - Conshohocken" : "PA",
    "'feine - Merenda Box" : "PA",
    "'feine - Skippack" : "PA",
    "359 Grab 'N Go" : "PA",
    "3J's Coffee" : "PA",
    "5 West Cafe" : "MD",
    "Achenbach's Pastries, Inc." : "PA",
    "Alabaster Coffee Roaster" : "PA",
    "American Ice Co. Cafe" : "MD",
    "Amy & Alex's Homemade Ice Cream & Coffee" : "WV",
    "Ancestor Coffeehouse - Lebanon" : "PA",
    "Ancestor Coffeehouse - Palmyra" : "PA",
    "Aroma Cafe" : "VA",
    "Artifact Coffee" : "MD",
    "Assateague Island Surf Shop & Cafe" : "MD",
    "ASSETS" : "PA",
    "Athena's Kafenio" : "PA",
    "Aveley Farms Coffee" : "MD",
    "Avenue 209 Coffee House" : "PA",
    "Back Creek Cafe & Boat Supply" : "MD",
    "Backyard Beans Coffee Co - Ambler" : "PA",
    "Bagel Lovers" : "PA",
    "Bagel Meister" : "MD",
    "Bageleddis" : "NJ",
    "Bagery" : "MD",
    "Baked n Brewed" : "PA",
    "Bakery 350" : "PA",
    "Baristi Coffee Roasters" : "PA",
    "Battle Grounds Bakery and Coffee" : "WV",
    "Bean Rush Cafe - Crownsville" : "MD",
    "Bean Rush Cafe - Glen Burnie" : "MD",
    "Beanbury" : "NJ",
    "Beans Beans-The Musical Coffee Cart" : "N/A",
    "Beans in the Belfry" : "MD",
    "Bee Silky Soap Gift Shoppe" : "PA",
    "Bella Vita Coffee & Cream" : "PA",
    "Belmont Bean-Belmont St." : "PA",
    "Benchwarmers Coffee" : "PA",
    "Bing's Bake and Brew" : "DE",
    "Birdie's Cafe" : "MD",
    "Bistro Barberet & Bakery" : "PA",
    "Black Acres Roastery" : "MD",
    "Black Rail Coffee" : "NJ",
    "Black Street Coffee Roasters" : "MD",
    "Blank Street - 14th St" : "DC",
    "Blank Street - 7th St" : "NY",
    "Blank Street - Connecticut Ave" : "DC",
    "Blank Street - M St." : "DC",
    "Blank Street - Prospect St" : "DC",
    "Blessed By Design" : "N/A",
    "Blessing Cafe" : "VA",
    "Bliss Coffee Lounge" : "NJ",
    "Blocker's Coffee House" : "PA",
    "Blossom Cafe" : "PA",
    "Blue Rooster Cafe" : "MD",
    "Blue Waters Caribbean & Seafood Grill" : "MD",
    "Bobapop - Alexandria" : "VA",
    "BoBaPop - Falls Church" : "VA",
    "BoBaPop - Germantown" : "VA",
    "BoBaPop Tea Bar - Gaithersburg" : "MD",
    "Bobby Chez - Cherry Hill" : "NJ",
    "Bobby Chez - Delran" : "NJ",
    "Bon Fresco - Gaither Road" : "MD",
    "Bon Fresco - Guilford Road" : "MD",
    "Bon Fresco - Oakland Mills Road" : "MD",
    "Boro Coffee Co" : "PA",
    "Boxcar Burgers - Brunswick" : "MD",
    "Boxcar Burgers - Frederick" : "MD",
    "Brew Boxx - Millersburg" : "PA",
    "Brewed Awakening-Royersford" : "PA",
    "Brio Coffeehouse - Greencastle" : "PA",
    "Brio Coffeehouse - Waynesboro" : "PA",
    "Britton Coffee Co - Hanover" : "PA",
    "Britton Coffee Co - McSherrystown" : "PA",
    "Brock & Co - Lutron Electronics Co, Inc" : "PA",
    "Brock & Co - PJM Cafe" : "N/A",
    "Brookland Grill" : "DC",
    "Brown's Concessions-The Oasis" : "N/A",
    "Browns Orchards and Farmers Market" : "PA",
    "Buffalo Brew" : "PA",
    "Bushel & Peck Southern Sweet Tea" : "MD",
    "Butter and Bean - Southern Mkt" : "PA",
    "Butter and Bean - Tanger Outlets" : "PA",
    "Cafe Alice" : "DC",
    "Cafe Blessing - KCPC Cafe" : "NY",
    "Cafe Con Bagel" : "DC",
    "Cafe Flora" : "NJ",
    "Cafe Lemont" : "PA",
    "Cafe Levantine" : "VA",
    "Cafe Lucky Bones" : "NJ",
    "Cafe Nola" : "MD",
    "Cafe Ole" : "PA",
    "Cafe on the Bay" : "MD",
    "Cafe One Eight" : "PA",
    "Cafe Rx" : "NJ",
    "Cafe the Lodge" : "PA",
    "Cafein - Centreville" : "VA",
    "Caffe Amouri" : "VA",
    "Cake & Cup Bake Shoppe" : "PA",
    "Calm Waters Coffee-Newtown" : "PA",
    "Calm Waters Coffee Roasters-Bristol" : "PA",
    "Calvary Temple" : "PA",
    "Cannon Coffee - Potomac" : "MD",
    "Cannon Coffee - Robinwood" : "MD",
    "Cantina Bambina" : "DC",
    "Capital Joe - Mechanicsburg" : "PA",
    "Capo I Italian Deli - Florida Ave" : "DC",
    "Capo II-Pennsylvania Ave (Western Mkt)" : "DC",
    "Capo III-Tyson's Corner" : "VA",
    "Capo IV - Potomac" : "MD",
    "Capo V - Alexandria" : "VA",
    "Casey's Coffee - 23rd Street" : "DC",
    "Casey's Coffee - College Park" : "MD",
    "Casey's Coffee - E Street" : "DC"
}
df4["State"] = df4["Customer"].map(shop_to_state)
df4 = df4.merge(pumpkin_columns, on = "Customer", how ="left")
print(df4)
df4.to_excel("/Users/nmall/Desktop/HK Stuff/HKSalesData.xlsx", index=False)
# pumpkin_columns.to_excel("HKPumpkinSales.xlsx", index=False)
# salesByDate.to_excel("HKsalesbyinvoice.xlsx", index=False)
'''
salesByDate["Date"] = pd.to_datetime(salesByDate["Date"])
salesByDate.rename(columns={'Date': 'ds', 'Sales Total': 'y'}, inplace = True)
modelData = salesByDate[["ds", "y"]]
modelData.groupby('ds')['y'].sum().reset_index()
model = Prophet()
model.fit(modelData)
future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)
model.plot(forecast)
plt.show()
model.plot_components(forecast)
plt.show()

forecast['ds'] = pd.to_datetime(forecast['ds'])

# Filter for months Jan-Aug for 2024 and 2025
forecast_filtered = forecast[(forecast['ds'].dt.year.isin([2024, 2025])) &
                             (forecast['ds'].dt.month <= 8)]

# Extract Year and Month
forecast_filtered['Year'] = forecast_filtered['ds'].dt.year
forecast_filtered['Month'] = forecast_filtered['ds'].dt.strftime('%b')

# Define month order for correct chronological plotting
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
forecast_filtered['Month'] = pd.Categorical(forecast_filtered['Month'], categories=month_order, ordered=True)

# Group by Year and Month and calculate the mean forecasted sales (yhat)
monthly_forecast = forecast_filtered.groupby(['Year', 'Month'])['yhat'].mean().unstack(level=0)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(monthly_forecast.index, monthly_forecast[2024], label='2024', marker='o')
plt.plot(monthly_forecast.index, monthly_forecast[2025], label='2025', marker='o')

# Customize the plot
plt.title('Monthly Sales Forecast Comparison (Jan-Aug)')
plt.xlabel('Month')
plt.ylabel('Forecasted Sales Amount')
plt.xticks(monthly_forecast.index)  # Set x-axis to show months in correct order
plt.legend()

# Display the plot
plt.grid(True)
plt.tight_layout()
plt.show()
'''