import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Protein Length Explorer", layout="wide")

@st.cache_data
def load_data():
	df = pd.read_csv("length_counts.tsv", sep='\t')

	df.columns = ['length', 'count']
	return df

df = load_data()
max_protein_length = df['length'].max()

st.sidebar.header("Ρυθμίσεις Γραφήματος")

#Slider για το μήκος του bin
binning_mode = st.sidebar.radio("Μέγεθος Κατανομής", ("Γραμμικά Bins", "Λογαριθμικά Bins","Εστιασμένο 5-1000"))

#Checkbox για να δεις αν θελεις να διαλέξεις τη λογαριθμική κλίμακα
use_log_scale = st.sidebar.checkbox("Λογαριθμική Κλίμακα", value=False)

if binning_mode=="Γραμμικά Bins":
	bin_width = st.sidebar.slider("Πλάτος Bin", min_value=10, max_value=2000, value=200, step=10)
	df['bin_start'] = (df['length'] // bin_width) * bin_width
	binned_df = df.groupby('bin_start')['count'].sum().reset_index()

#Δημιουργία του διαγράμματος
	fig = px.bar(binned_df, x='bin_start', y='count',
	labels={'bin_start': f"Μήκος Πρωτεινης ",'count': 'Πλήθος Πρωτεινων'},
	title="Γραμμικό Ιστόγραμμα ",
	log_y=use_log_scale)

#Κάνουμε τις μπάρες να εφάπτονται
	fig.update_layout(bargap=0)
	fig.update_traces(marker_color='steelblue', marker_line_width=0)
	fig.update_xaxes(nticks=30)
elif binning_mode =="Λογαριθμικά Bins":
#Ρυθμίσεις για το Λογαριθμικό View
    log_bins_count = st.sidebar.slider("Αριθμός Λογαριθμικών Bins", min_value=10, max_value=100, value=30, step=1)
    df_log = df[df['length'] > 0]
    bins_edges = np.logspace(np.log10(1), np.log10(df_log['length'].max() + 1), num=log_bins_count + 1 )
    df_log['log_bin'] = pd.cut(df_log['length'], bins=bins_edges, include_lowest=True, right=False)

    binned_df = df_log.groupby('log_bin')['count'].sum().reset_index()

    binned_df['bin_start'] = binned_df['log_bin'].apply(lambda x: x.left)
    fig = px.bar(binned_df, x='bin_start', y='count', labels={'bin_start': 'Μήκος Πρωτεινης ', 'count': 'Πλήθος Πρωτεινών'}, title="Λογαριθμικό Ιστόγραμμα ", log_y=use_log_scale, log_x=True )

    fig.update_traces(marker_color='firebrick', marker_line_width=0)
    fig.update_xaxes(nticks=30)
else:
    zoom_bin_width = st.sidebar.slider("Πλάτος Bin (Zoom)", min_value=1, max_value=50, value=5, step=1)
    # Κρατάμε μόνο τις πρωτεΐνες από 100 έως 500
    df_focus = df[(df['length'] >= 5) & (df['length'] <= 1000)].copy()
    # Φτιάχνουμε γραμμικά bins
    df_focus['bin_start'] = (df_focus['length'] // zoom_bin_width) * zoom_bin_width
    binned_df = df_focus.groupby('bin_start')['count'].sum().reset_index()

    fig = px.bar(binned_df, x='bin_start', y='count',
                 labels={'bin_start': 'Μήκος Πρωτεΐνης ', 'count': 'Πλήθος Πρωτεϊνών'},
                 title=f"Εστιασμένο Ιστόγραμμα (5 - 1000 αμινοξέα)",
                 log_y=use_log_scale)
    fig.update_layout(bargap=0)
    fig.update_traces(marker_color='mediumseagreen', marker_line_width=0)
    fig.update_xaxes(dtick=100)
st.plotly_chart(fig, use_container_width=True)

