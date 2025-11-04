import streamlit as st
from storage import init_db, add_monitor, list_monitors, get_checks
from monitor import MonitorWorker
import pandas as pd
import plotly.express as px

init_db()

st.set_page_config(page_title='API Uptime Monitor', layout='wide')
st.title('API Uptime Monitoring')


# start background worker (singleton stored in session state)
if 'worker' not in st.session_state:
    st.session_state.worker = MonitorWorker()
    st.session_state.worker.start()


with st.sidebar:
    st.header('Add Monitor')
    url = st.text_input('API URL')
    interval = st.number_input('Interval (minutes)', min_value=1, value=5)
    if st.button('Add'):
        if url:
            add_monitor(url.strip(), int(interval))
            st.success('Monitor added. It will be checked shortly.')

    st.markdown('---')
    st.write('Background worker is running in session state.')


st.header('Monitors')
monitors = list_monitors()
if not monitors:
    st.info('No monitors yet. Add one from the sidebar.')
else:
    cols = st.columns([3,1,1,2])
    for m in monitors:
        with st.container():
            c1, c2, c3, c4 = st.columns([3,1,1,2])
            c1.subheader(m['url'])
            c2.metric('Status', m['last_status'] or 'Unknown')
            c3.write(m['interval_minutes'])
            if c4.button('View Logs', key=f'logs_{m["id"]}'):
                checks = get_checks(m['id'], limit=200)
                if checks:
                    df = pd.DataFrame(checks)
                    df['checked_at'] = pd.to_datetime(df['checked_at'])
                    st.write(df.head(50))
                    if 'response_time_ms' in df.columns and df['response_time_ms'].notna().any():
                        fig = px.line(df.sort_values('checked_at'), x='checked_at', y='response_time_ms', title=f"Response times — {m['url']}")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info('No checks yet for this monitor.')


st.markdown('---')


st.header('Quick Test')
st.write('Test a URL immediately (one-off)')
input_url = st.text_input('URL to test now')
if st.button('Run Test') and input_url:
    # perform a single blocking check and show result
    from monitor import check_once
    status_text, status_code, elapsed = check_once({'url': input_url, 'id': -1})
    st.success(f'Result: {status_text} — {status_code} — {elapsed} ms')