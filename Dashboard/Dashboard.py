import streamlit as st
import pandas as pd
# import plotly.graph_objects as go
import csv
## new 


# import plotly.graph_objects as go
# from ydata_profiling import ProfileReport
# from streamlit_pandas_profiling import st_profile_report
import datetime as dt

from data_fetcher import (
    fetch_data_not_working_hour,fetch_data_starpay_edited,fetch_data_CRM_total, fetch_data_driver_not_available_a, fetch_data_driver_not_available_b,
    fetch_data_all_cancellation_count, fetch_data_all_incomplete_orders, fetch_data_all_more_than_60_min,
    fetch_data_all_more_than_150, fetch_data_all_on_time, fetch_data_all_crm_cancelation, fetch_data_all_unsafe,
    fetch_data_all_other_reason, fetch_data_all_distance_too_long, fetch_data_all_pos_discount, fetch_data_all_handover,
    fetch_data_all_delivery_timestamp, fetch_data_all_men_ratings, fetch_data_all_pick_up_35min, fetch_data_incomplete_driver,
    fetch_data_morethan_90, fetch_data_order_after_2, fetch_data_placed_at_morethan_40min, fetch_data_possible_spammer,
    fetch_data_resturant_rating, fetch_data_c6, fetch_data_c9, fetch_data_mube,fetch_data_crm,fetch_data_acc_ass, fetch_data_accive_status,
    fetch_data_telebirr_edited,fetch_data_telebirr_canceled,fetch_data_arifpay_canceled,fetch_data_chapa_canceled,
    fetch_data_R9,fetch_data_R12,fetch_data_R47,fetch_data_CRM_conve_agent,fetch_data_CRM_total,fetch_data_CRM_total_month,
    fetch_data_mube_compensation,fetch_data_removeed_deduction,fetch_data_ussd_canceled,fetch_data_telebirr_ussd_edited,
    fetch_data_timestamp,fetch_data_ontime,fetch_data_all_cancellation_byorder,fetch_data_to_download,
    fetch_data_failed_order,fetch_data_campaing_code,fetch_data_driver_rating,fetch_data_m_pesa_canceled,fetch_data_m_pesa_edited,
    fetch_failed_transactions,fetch_today_order,fetch_new_user,fetch_data_cancel_no_order,fetch_data_R54,fetch_data_order_after_4_30,
    fetch_data_pos_orders,fetch_data_arif_pay_edited,fetch_data_chapa_edited,fetch_data_split_canceled,fetch_data_split_edited,
    fetch_data_cancled_on_not_samed_date,fetch_filtered_data,fetch_data_cancled_after_22,fetch_data_Assigned,fetch_time_stamp,
    fetch_driver_bag_check,fetch_customer_transactions_by_session,fetch_Driver_transactions_by_session,fetch_data_BD_report,fetch_data_starpay_canceled
)

# Set up the Streamlit app
st.set_page_config(page_title="beU Delivery Dashboard", layout="wide")

st.title("beU Delivery Dashboard")

def filter_date_data(query_option,):
    # User selects query option
    query_option = st.selectbox("Select Data to View:", list(query_to_function.keys()))

    # Fetch the data
    fetch_function = query_to_function.get(query_option)
    if fetch_function:
                # Special case for fetch_data_timestamp, as it needs order_ids
        if fetch_function == fetch_data_timestamp:
            st.subheader("Check Order Timestamp")
            input_order_ids = st.text_input("Enter Order ID(s), comma-separated:")

            if input_order_ids:
                try:
                    order_ids = [int(x.strip()) for x in input_order_ids.split(",")]
                    result_df = fetch_data_timestamp(order_ids)
                    if not result_df.empty:
                        st.dataframe(result_df)
                        st.download_button("Download Result", result_df.to_csv(index=False), "order_timestamps.csv", "text/csv")
                    else:
                        st.warning("No data found for the provided Order ID(s).")
                except Exception as e:
                    st.error(f"Error fetching data: {e}")
        elif   fetch_function == fetch_data_campaing_code:
                st.subheader("Check Users by Campaign Code and Date")

                input_code = st.text_input("Enter Campaign Code:")
                selected_date = st.date_input("Select Date")

                if input_code and selected_date:
                    try:
                        result_df = fetch_data_campaing_code(input_code.strip(), selected_date)

                        if not result_df.empty:
                            # Count of 'Yes' in is_new_user
                            new_user_count = (result_df['is_new_user'] == 'Yes').sum()
                            
                            # Total order count
                            total_orders = result_df['order_count'].sum()
                            
                            unique_users = result_df['user_id'].nunique()

                            # Show summary metrics
                            st.metric("New Users (Yes)", new_user_count)
                            st.metric("Total Orders", total_orders)
                            st.metric("Unique Users", unique_users)

                            # Optionally show the full table below
                            # st.dataframe(result_df)

                            # Optionally allow download
                            # st.download_button("Download Result", result_df.to_csv(index=False), "campaign_users.csv", "text/csv")
                        else:
                            st.warning("No data found for the provided inputs.")
                    except Exception as e:
                        st.error(f"Error fetching data: {e}")

        elif fetch_function == fetch_driver_bag_check:
            st.subheader("Driver Bag Check")
            input_phone = st.text_input("Enter Phone Number by +251 format :")
            
            if input_phone:
                try:
                    result_df = fetch_driver_bag_check(input_phone.strip())
                    if not result_df.empty:
                        st.dataframe(result_df, use_container_width=True)
                        
                        
                    else:
                        st.warning("No data found for the provided phone number.")
                except Exception as e:
                    st.error(f"Error fetching data: {e}")
        
        elif fetch_function == fetch_Driver_transactions_by_session or fetch_function == fetch_customer_transactions_by_session:
            st.subheader("Transactions by session")
            input_session_id = st.text_input("Enter Session ID:")

            if input_session_id:
                try:
                    result_df = fetch_function(input_session_id.strip())
                    if not result_df.empty:
                        st.dataframe(result_df, use_container_width=True)
                    else:
                        st.warning("No data found for the provided session ID.")
                except Exception as e:
                    st.error(f"Error fetching data: {e}")
        elif fetch_function == fetch_data_CRM_total:
            st.subheader("CRM Total by Date")
            col1, col2 = st.columns(2)
            today = dt.date.today()
            one_month_ago = today - dt.timedelta(days=30)

            start_date = col1.date_input("Start Date", one_month_ago)
            end_date = col2.date_input("End Date", today)

            if start_date and end_date:
                try:
                    result_df = fetch_data_CRM_total(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                    if not result_df.empty:
                        st.dataframe(result_df, use_container_width=True)
                        csv_data = result_df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv_data,
                            file_name=f"{query_option}_{start_date}_to_{end_date}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("No data found for the provided date range.")
                except Exception as e:
                    st.error(f"Error fetching data: {e}")

        else:
            data = fetch_function()
            if data is not None and not data.empty:
                # Convert 'order_Date' to datetime and then to date only
                if "order_Date" in data.columns:
                    data["order_Date"] = pd.to_datetime(data["order_Date"], format="%Y-%m-%d").dt.date
                    
                    # Date Filter
                    st.write("### Filter by Date")
                    unique_dates = sorted(data["order_Date"].unique(), reverse=True)  # Unique dates sorted in descending order
                    selected_date = st.selectbox("Select a Date:", unique_dates)
                    
                    # Filter the data based on the selected date
                    filtered_data = data[data["order_Date"] == selected_date]
                    
                    st.write(f"### {query_option} for {selected_date}")
                    st.dataframe(filtered_data, use_container_width=True)
                    
                    # Add download button for filtered data
                    excel = filtered_data.to_csv(index=False)
                    st.download_button("Download CSV", data=excel, file_name=f"{query_option}_{selected_date}.csv", mime="text/csv")
                else:
                    st.dataframe(data)
                    # # Convert to CSV string
                    # csv = data.to_csv(index=False)

                    # # Create the download button using the CSV string directly
                    # st.download_button(
                    #     label="Download CSV",
                    #     data=csv,
                    #     file_name="data_export.csv",
                    #    
                    # mime="text/csv"
                    # )
                    # Convert to CSV string with proper quoting
                #    st.dataframe(data)

                    csv_str = data.to_csv(
                        index=False,
                        quoting=csv.QUOTE_MINIMAL,
                        escapechar='\\'
                    )

                    st.download_button(
                        label="Download CSV",
                        data=csv_str,
                        file_name="data_export.csv",
                        mime="text/csv"
                    )
            else:
                st.error(f"No data available for {query_option}.")
    else:
        st.error("Invalid query option selected.")

    # Function to filter data by date and area manager

def filter_area_manager_data(query_option):
    # Fetch the data
    fetch_function = query_to_function.get(query_option)
    if fetch_function:
        data = fetch_function()
        if data is not None and not data.empty:
            if "area" in data.columns:
                # If 'order_Date' is in the data, filter by date
                if "order_Date" in data.columns:
                    # Convert 'order_Date' to datetime and then to date only
                    data["order_Date"] = pd.to_datetime(data["order_Date"], format="%Y-%m-%d").dt.date
                    
                    # Date Filter (only if the selected query requires it)
                    if query_option != "Active Status":  # Skip date filtering for Active Status
                        st.write("### Filter by Date")
                        unique_dates = sorted(data["order_Date"].unique(), reverse=True)  # Unique dates sorted in descending order
                        selected_date = st.selectbox("Select a Date:", unique_dates)

                        # Filter the data based on the selected date
                        filtered_data = data[(data["area"].isin(selected_districts)) & (data["order_Date"] == selected_date)]
                        st.write(f"### {query_option} for {selected_person} ({', '.join(selected_districts)}) on {selected_date}")
                    else:
                        # No date filter for Active Status
                        filtered_data = data[data["area"].isin(selected_districts)]
                        st.write(f"### {query_option} for {selected_person} ({', '.join(selected_districts)})")

                else:
                    # If 'order_Date' column doesn't exist, just filter by area
                    filtered_data = data[data["area"].isin(selected_districts)]
                    st.write(f"### {query_option} for {selected_person} ({', '.join(selected_districts)})")

                st.dataframe(filtered_data, use_container_width=True)

                # Add download button for filtered data
                csv_data = filtered_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"{query_option}_{selected_person}.csv",  # Adjust the filename when no date is selected
                    mime="text/csv"
                )
            else:
                st.warning("'area' column is missing in the data.")
        else:
            st.error(f"No data available for {query_option}.")
    else:
        st.error("Invalid query option selected.")

category = st.sidebar.radio("Select Category:", ["Delivery Data", "Call Center","Area Manager","Payment issues","Dashboard","Marketing","Customer Support"])

if category == "Delivery Data":
    st.subheader("Delivery Data")

    # Mapping query options to fetch functions for Delivery Data
    query_to_function = {
        "All Cancellation Count": fetch_data_all_cancellation_count,
        "All delivery timestamp": fetch_data_all_delivery_timestamp,
        "Created to picked up more than 35 min": fetch_data_all_pick_up_35min,
        "CRM cancelation": fetch_data_all_crm_cancelation,
        "Delivery men ratings daily": fetch_data_all_men_ratings,
        "Distance too long": fetch_data_all_distance_too_long,
        "Driver Not Available(After)": fetch_data_driver_not_available_a,
        "Driver Not Available(Before)": fetch_data_driver_not_available_b,
        "Handover not null but cancled": fetch_data_all_handover,
        "Incomplete orders with driver": fetch_data_incomplete_driver,
        "Incomplete Orders": fetch_data_all_incomplete_orders,
        "More than 150 orders": fetch_data_all_more_than_150,
        "More than 60 Min orders": fetch_data_all_more_than_60_min,
        "Morethan 90 min": fetch_data_morethan_90,
        "Not Working Hour": fetch_data_not_working_hour,
        "On time": fetch_data_all_on_time,
        "Orders after 20:00:00": fetch_data_order_after_2,
        "Other reason": fetch_data_all_other_reason,
        "Placed at to accepted in more than 35 min": fetch_data_placed_at_morethan_40min,
        "Pos discount": fetch_data_all_pos_discount,
        "Possible spammer": fetch_data_possible_spammer,
        "Timestamp":fetch_data_timestamp,
        "Removed Deduction":fetch_data_removeed_deduction,
        "Restaurant rating": fetch_data_resturant_rating,
        "Unsafe": fetch_data_all_unsafe,
        "download all data":fetch_data_to_download,
        "Driver Rating":fetch_data_driver_rating,
        "Assigned Orders":fetch_data_Assigned,
        "Driver bag check":fetch_driver_bag_check
        
        }

    filter_date_data(query_to_function)

elif category == "Call Center":
    # Call Center Data
    st.subheader("Call Center Data")
    
    query_to_function ={
        "C6: Others": fetch_data_c6,
        "c9: CRM forgot to order the meal": fetch_data_c9,
        "R5: (CRM) Not receiving phone call | BEFORE ":fetch_data_crm,
        "R9:(CRM) Ordered by mistake | BEFORE ":fetch_data_R9,
        "R12: (CRM) Repeated order | BEFORE ":fetch_data_R12,
        "R47:(CRM) Customer not willing to pay using mobile banking":fetch_data_R47,
        "More than 50 minute cancellation": fetch_data_mube,
        "CRM Conversation agent":fetch_data_CRM_conve_agent,
        "CRM Total by date":fetch_data_CRM_total,
        "CRM Total by month":fetch_data_CRM_total_month,
        "Mube compensation":fetch_data_mube_compensation,
        "Timestamp":fetch_data_timestamp,
        "Cancelled and did not order":fetch_data_cancel_no_order,
        "Restaurant qualitty issue":fetch_data_R54,
        "POS Orders":fetch_data_pos_orders,
        "Cancelled on different date ":fetch_data_cancled_on_not_samed_date,
        "Cancelled after 22:00":fetch_data_cancled_after_22,
        "Admin_log":fetch_time_stamp
    }
  
    filter_date_data(query_to_function)

elif category == "Area Manager":
    st.subheader("Area Manager Data")
    
    # Updated district mapping
    district_mapping = {
        "Sami/G": [
            "Piyassa", "Paster", "Motor Orders", "Sarbet", "Mexico", "Bethel", "Meskel Flower", "6Kilo", "kazanchis"
        ],
        "Elshaday": [
            "Gerji", "Megenagna", "22", "Lafto", "Jemo"
        ],
        "Bisrat": [
            "Bole", "Saris", "Kality", "Bulbula", "Civil Service", "Abado", "Ayat", "Summit", "Tulu Dimtu"
        ]
    }

    # Dropdown to select Area Manager
    selected_person = st.sidebar.selectbox("Select an Area Manager:", list(district_mapping.keys()))

    # Fetch the districts for the selected person
    selected_districts = district_mapping[selected_person]

    # Query mapping for the Area Manager section
    query_to_function = {
        "Accepted and Assigned Percentage": fetch_data_acc_ass,
        "Active Status": fetch_data_accive_status
    }
    
     # Call the filtering function
    query_option = st.selectbox("Select Data to View:", list(query_to_function.keys()))
    filter_area_manager_data(query_option)
    # filter_date_data(query_to_function)

elif category == "Payment issues":
    st.subheader("Paid but Cancelled and edited ")
    
    query_to_function = {
        "Telebirr paid but edited":fetch_data_telebirr_edited,
        "Telebirr paid but cancelled":fetch_data_telebirr_canceled,
        "Arifpay paid but cancelled":fetch_data_arifpay_canceled,
        "Chapa paid but cancelled":fetch_data_chapa_canceled,
        "Telebirr-ussd cancelled users":fetch_data_ussd_canceled,
        "Telebirr-ussd paid but edited":fetch_data_telebirr_ussd_edited,
        "M-Pessa-ussd cancelled users":fetch_data_m_pesa_canceled,
        "M-Pessa-ussd paid but edited":fetch_data_m_pesa_edited,
        "Failed Transactions":fetch_failed_transactions,
        "Arifpay paid but edited":fetch_data_arif_pay_edited,
        "Chapa paid but edited":fetch_data_chapa_edited,
        "Split paid but edited":fetch_data_split_edited,
        "Split cancelled":fetch_data_split_canceled,
         "Customer transactions by session":fetch_customer_transactions_by_session,
        "Driver transactions by session":fetch_Driver_transactions_by_session,
        "Star Pay paid but canceled":fetch_data_starpay_canceled,
        "Star Pay edited orders":fetch_data_starpay_edited
        
    }
    
    filter_date_data(query_to_function)

elif category == "Marketing":
    st.title("Business Developer Dashboard")
    query_to_function = { "All Cancellation by Order ID":fetch_data_all_cancellation_byorder,
                         "Failed Orders":fetch_data_failed_order,
                         "coupoun code":fetch_data_campaing_code,
                        #  "Retention":fetch_retention,
                         "new users by date":fetch_new_user,
                         "Today's Orders":fetch_today_order,
                         "Orders after 04:30":fetch_data_order_after_4_30,
                         "BD Report":fetch_data_BD_report}
    filter_date_data(query_to_function)
    
elif category == "Customer Support":
    st.title("Customer Support Dashboard")
    query_to_function = {
        "Total Order Count for Customer Support based on beU Individual and Food Order": fetch_data_CRM_total,
    }
    filter_date_data(query_to_function)

# elif category == "All sales":

#     st.title("Order Overview Dashboard")

#     # === Filters ===
#     col1, col2 = st.columns(2)
#     today = dt.date.today()
#     one_month_ago = today - dt.timedelta(days=30)

#     start_date = col1.date_input("Start Date", one_month_ago)
#     end_date = col2.date_input("End Date", today)

#     # Load BD and Restaurant filter options dynamically
#     with st.spinner("Loading filter options..."):
#         bd_options = get_unique_bds()
#         restaurant_options = get_unique_restaurants()
#     col3, col4 = st.columns(2)
#     bd_filter = col3.multiselect("Business Developer", options=bd_options)
#     rest_filter = col4.multiselect("Restaurant Name", options=restaurant_options)
#     order_id_filter = st.text_input("Order ID (comma-separated)")

#     order_ids = [oid.strip() for oid in order_id_filter.split(',') if oid.strip()]

#     # === Fetch Data ===
#     with st.spinner("Fetching filtered data..."):
#         df = fetch_filtered_data(
#             start_date.strftime('%Y-%m-%d'),
#             end_date.strftime('%Y-%m-%d'),
#             bd_list=bd_filter if bd_filter else None,
#             restaurant_list=rest_filter if rest_filter else None,
#             order_ids=order_ids if order_ids else None
#         )

#     # === Process & Display ===
#     df['created_at'] = pd.to_datetime(df['created_at'])
#     df['revenue'] = df['price'] * df['quantity']
#     df['delivery_charge'] = df.get('delivery_charge', 0)

#     col1, col2, col3 = st.columns(3)
#     col1.metric("🧾 Total Orders", f"{df['id'].nunique():,}")
#     col2.metric("💰 Revenue", f"{df['revenue'].sum():,.2f} ETB")
#     col3.metric("🚚 Delivery Revenue", f"{df['delivery_charge'].sum():,.2f} ETB")

#     # st.markdown("### Preview of Filtered Data")
#     # st.dataframe(df.head(50))
