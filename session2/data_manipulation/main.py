import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


'''In this example, we are going to make a smll program that...

'''

def main():

    # --- Let's use NumPy to create some data ---
    print("--- NumPy Random Data Generation ---")

    # Create a NumPy array from a list of numbers
    fixed_array = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    print("Fixed Array:", fixed_array)
    # Create a NumPy array with random values between 0 and 100
    random_array = np.random.randint(0, 100, size=10)
    print("Random Array:", random_array)

    # We can directly add the two arrays together as they are the same size
    add_array = fixed_array + random_array
    print("Add Array:", add_array)

    try:
        random_array2 = np.random.randint(0, 100, size=11)
        add_array2 = fixed_array + random_array2
    except ValueError as e:
        print("But it will fail if the arrays are not the same size")

    # In addition to operations between arrays, we can also apply functions to the arrays that will be applied element-wise.
    #For example let's define a simple polynomial function f(x) = x^2 + 3x + 5 (we are using a lambda function here for simplicity)
    f = lambda x: x** + 3*x +5
    # We can simply apply this function to the arrays
    f_fixed = f(fixed_array)
    print("f(Fixed Array):", f_fixed)
    f_random = f(random_array)
    print("f(Random Array):", f_random)

    # Now we could create also another function g that would return the square root of the input
    g = lambda x: np.sqrt(x)
    # We can do then some random operations with this like appylying both functions to our arrays and then subtracting the results:
    retArray = g(f(fixed_array)) - g(f(random_array))
    print("Result Array:", retArray)

    # As you can see, while these are operations that we could do with lists, NumPy allows us to do them in a more efficient way and with less code, with a more mathematical approach.
    # In addition, numpy is optimized for performance, so these operations are generally faster than using Python lists.

    # Numpy also provides an easy way to get statistics on the data, like the mean, median, standard deviation, etc.
    print("--- NumPy Statistics ---")
    print(f"Mean of Fixed Array: {np.mean(fixed_array)}")
    print(f"Median of Fixed Array: {np.median(fixed_array)}")
    print(f"Standard Deviation of Fixed Array: {np.std(fixed_array)}")
    print(f"Variance of Fixed Array: {np.var(fixed_array)}")  

    # --- Let's use Pandas to create a DataFrame ---
    # We are going to use our fixed_array and random_array to create a new dataframe
    print("--- Pandas DataFrame Creation ---")
    data = {
        'fixed': fixed_array,
        'random': random_array,
        'f_fixed': f_fixed,
        'f_random': f_random
    }

    df = pd.DataFrame(data)
    print("DataFrame:\n", df)

    # With this dataframe, we can for example get some statistics on the data   
    print("--- Pandas Statistics ---")
    print(df.describe())

    # We can also apply functions to the dataframe, like we did with NumPy
    # For simple functions like our g function, we can use the apply method like in numpy:
    g_df = g(df)
    print("DataFrame:\n", g_df)

    # But for more complex functions, we can use the apply method that will iterate over the rows or columns of the dataframe:
    g_df2 = df.apply(g)
    print("DataFrame:\n", g_df2)

    # We can also add new columns to the dataframe with the results of the function on one or more columns:
    df['g_fixed'] = g(df['fixed'])
    df['g_random'] = g(df['random'])
    df['gf_fixed'] = g(df['f_fixed'])
    df['gf_random'] = g(df['f_random'])
    df['gf_substract'] = df['gf_fixed'] - df['gf_random']
    gm = lambda x,y: g(x) - g(y)
    df['gf_substract2'] = gm(df['f_fixed'], df['f_random'])
    print("DataFrame:\n", df)

    # --- Let's use Pandas to work with an existing dataframe  ---

    # Read the CSV file into a DataFrame
    df = pd.read_csv('data.csv', index_col=0)

    # Convert the 'Datetime' column to datetime format
    df['Datetime'] = pd.to_datetime(df['Datetime'])

    # Print the first and last few rows of the DataFrame
    print(df.head())
    print(df.tail())

    # Print the DataFrame information automatically calculated by pandas
    print(df.describe())


    # Plot the temperature over time in fig1.png
    df.plot(x='Datetime', y='Hourly_Temp', kind='line')
    plt.xlabel('Datetime')
    plt.ylabel('Temperature')
    plt.title('Temperature over Time')
    plt.savefig('fig1.png', bbox_inches='tight', dpi=300) 


    # Now let's filter the data for a specific day and plot it in fig2.png
    day = '2022-01-04'
    df_filtered = df[df['Datetime'].dt.date == pd.to_datetime(day).date()]
    df_filtered.plot(x='Datetime', y='Hourly_Temp', kind='line')
    plt.savefig('fig2.png', bbox_inches='tight', dpi=300) 

    #Next we will plot the average temperature for each day in fig3.png
    ## Add a new column with the date only
    df['Date'] = df['Datetime'].dt.date
    avg_df = df.groupby('Date')['Hourly_Temp'].mean().reset_index()
    avg_df.plot(x='Date', y='Hourly_Temp', kind='line')
    plt.savefig('fig3.png', bbox_inches='tight', dpi=300) 

    #Now we will save the average temperature data to a new CSV file (or overwrite the existing one)
    avg_df.to_csv('avg_data.csv')


    #Next we will plot the average temperature for each day in fig4.png
    ## Add a new column with the date only
    df['Date'] = df['Datetime'].dt.date
    max_df = df.groupby('Date')['Hourly_Temp'].max().reset_index()
    max_df.plot(x='Date', y='Hourly_Temp', kind='line')
    plt.savefig('fig4.png', bbox_inches='tight', dpi=300) 


    highest_temp_row = df.loc[df['Hourly_Temp'].idxmax()]
    print("\n--- Overall Highest Temperature Reading ---")
    print(highest_temp_row)

    # Find readings above a certain threshold (e.g., 22.5°C)
    above_threshold_readings = df[df['Hourly_Temp'] > 22.5]
    print("\n--- Readings Above 22.5°C ---")
    print(above_threshold_readings)

    # Example: Finding the top 3 hottest readings
    top_3_hottest = df.nlargest(3, 'Hourly_Temp')
    print("\n--- Top 3 Hottest Readings ---")
    print(top_3_hottest)


    # --- Now let's perform some statistics using NumPy ---


    print("--- NumPy Statistics on Temperature Data ---")
    # Calculate average temperature using NumPy
    average_temp = np.average(df['Hourly_Temp'])
    print(f"Overall Average Temperature (NumPy): {average_temp:.2f}°C")

    # Calculate median temperature using NumPy
    median_temp = np.median(df['Hourly_Temp'])
    print(f"Overall Median Temperature (NumPy): {median_temp:.2f}°C")

    # Calculate standard deviation of temperature using NumPy
    std_dev_temp = np.std(df['Hourly_Temp'])
    print(f"Overall Standard Deviation of Temperature (NumPy): {std_dev_temp:.2f}°C")

    # Calculate a percentile (e.g., 75th percentile)
    p75_temp = np.percentile(df['Hourly_Temp'], 75)
    print(f"75th Percentile Temperature (NumPy): {p75_temp:.2f}°C")
    
    #Calculate the difference in temperature between consecutive readings
    temp_changes = np.diff(df['Hourly_Temp'])
    print("First 5 temperature changes (degrees C):")
    print(temp_changes[:5])
    # Add a new column to the filtered DataFrame with the temperature change and plot it into fig5.png (again limited to a specific day)
    df['Temp_Change'] = df['Hourly_Temp'].diff()
    df_filtered = df[df['Datetime'].dt.date == pd.to_datetime(day).date()]
    df_filtered.plot(x='Datetime', y='Temp_Change', kind='line')
    plt.savefig('fig5.png', bbox_inches='tight', dpi=300) 
    
if __name__ == '__main__':
    main()