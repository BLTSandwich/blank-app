import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import streamlit as st

# Given data points
data_points = {
    32: 21,   # 32°F → 21 days
    -4: 2,    # -4°F → 2 days
    0: 4,     # 0°F → 4 days
    -15: 0    # -15°F → 0 days
}

def interpolate_freezing_time(temp_f):
    """
    Interpolate freezing time for a given temperature using the given data points.
    Returns days required to freeze bedbugs at the given temperature.
    """
    # Sort temperatures for interpolation
    temps = sorted(data_points.keys())
    days = [data_points[t] for t in temps]
    
    # Create interpolation function (cubic for smooth curve)
    f = interp1d(temps, days, kind='cubic', fill_value='extrapolate')
    
    # For temperatures below -15°F, use 0 days
    if temp_f <= -15:
        return 0
    # For temperatures above 32°F, return None (won't freeze)
    elif temp_f >= 32:
        return None  # Won't freeze at or above freezing point
    
    return max(0, float(f(temp_f)))  # Ensure non-negative

def main():
    st.set_page_config(page_title="Bedbug Freezing Calculator", layout="wide")
    
    st.title("❄️ Bedbug Freezing Time Calculator")
    st.markdown("""
    This calculator estimates how long it takes to freeze bedbugs at various temperatures.
    Based on empirical data:
    - 32°F: 21 days
    - 0°F: 4 days  
    - -4°F: 2 days
    - -15°F: 0 days
    """)
    
    # Create two columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Temperature Input")
        
        # Temperature input
        temp_input = st.number_input(
            "Enter temperature (°F):",
            min_value=-30.0,
            max_value=35.0,
            value=10.0,
            step=0.5,
            help="Temperature in Fahrenheit"
        )
        
        # Calculate freezing time
        freezing_time = interpolate_freezing_time(temp_input)
        
        # Display result
        if freezing_time is None:
            st.warning(f"At {temp_input}°F, bedbugs won't freeze (temperature is at or above freezing point)")
        else:
            days = round(freezing_time, 1)
            hours = round(freezing_time * 24, 1)
            
            st.success(f"### Result")
            st.metric(
                label=f"At {temp_input}°F",
                value=f"{days} days",
                delta=f"{hours} hours" if days > 0 else "Instant"
            )
            
            # Interpretation
            if days == 0:
                st.info("Bedbugs freeze instantly at this temperature")
            elif days <= 1:
                st.info("Rapid freezing - highly effective")
            elif days <= 7:
                st.info("Moderate freezing time - practical for treatment")
            else:
                st.info("Extended freezing time - may not be practical")
        
        # Quick reference table
        st.subheader("Quick Reference")
        ref_data = sorted(data_points.items())
        for temp, days in ref_data:
            st.write(f"**{temp}°F**: {days} day{'s' if days != 1 else ''}")
    
    with col2:
        st.header("Visualization")
        
        # Create temperature range for plotting
        plot_temps = np.linspace(-20, 33, 100)
        plot_days = []
        
        for temp in plot_temps:
            days = interpolate_freezing_time(temp)
            plot_days.append(days if days is not None else 0)
        
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
        
        # Plot 1: Main curve
        ax1.plot(plot_temps, plot_days, 'b-', linewidth=3, alpha=0.7)
        ax1.scatter(data_points.keys(), data_points.values(), 
                   color='red', s=100, zorder=5, label='Empirical Data')
        
        # Highlight user's temperature if applicable
        if interpolate_freezing_time(temp_input) is not None:
            user_days = interpolate_freezing_time(temp_input)
            if user_days is not None:
                ax1.scatter([temp_input], [user_days], 
                          color='green', s=200, zorder=10, 
                          label=f'Your Input: {temp_input}°F')
        
        ax1.set_xlabel('Temperature (°F)', fontsize=12)
        ax1.set_ylabel('Days to Freeze', fontsize=12)
        ax1.set_title('Bedbug Freezing Time vs Temperature', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.fill_between(plot_temps, plot_days, alpha=0.2, color='blue')
        
        # Plot 2: Logarithmic scale for better visualization
        ax2.plot(plot_temps, plot_days, 'r-', linewidth=2)
        ax2.set_yscale('log')
        ax2.set_xlabel('Temperature (°F)', fontsize=12)
        ax2.set_ylabel('Days to Freeze (log scale)', fontsize=12)
        ax2.set_title('Logarithmic Scale View', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Temperature zones
        st.subheader("Temperature Zones")
        zones = [
            ("Above Freezing (>32°F)", "No freezing occurs"),
            ("Freezing to Cold (32°F to 0°F)", "Slow freezing (weeks)"),
            ("Very Cold (0°F to -15°F)", "Fast freezing (days)"),
            ("Extreme Cold (<-15°F)", "Instant freezing")
        ]
        
        for zone, desc in zones:
            st.write(f"• **{zone}**: {desc}")

if __name__ == "__main__":
    main()