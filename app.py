import altair as alt
import pandas as pd
import streamlit as st
import seaborn as sns

@st.cache
def load_state(state: str) -> pd.DataFrame:
    df = pd.read_csv(f"data/dataset_{state}.csv", parse_dates=[4])
    return df


def main():
    states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
                'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
                'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
                'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
    age_groups = ['40-49', '50-64', '65+', '18-29', '30-39']
    electives = ['CYSTOSCOPY', 'CATARACT', 'KNEE REPLACEMENT', 'MASTECTOMY',
                    'CHOLECYSTECTOMY', 'HYSTEROSCOPY', 'HIP REPLACEMENT',
                    'PROSTATECTOMY', 'CABG', 'COSMETIC RECONSTRUCTION', 'COVID']

    st.title("Persimmon")
    state = st.sidebar.selectbox("Select state", states)
    """
    > Optimizing physician distribution between recurring elective surgeries and an ongoing pandemic
    """


    df = load_state(state)

    st.dataframe(df.head(10))
    st.info(f"Loaded {state} data! [{df.shape} matrix]")

    "## Patient"

    """
    This section gives you a functional overview of the data visualization and rough interaction between a patient
    and the platform. Essentially, the patient can enter basic information regarding his elective surgery, age group
    and state and will be presented with some helpful visual cues to highlight the trend in said elective surgery in comparison
    to not just other surgeries, but also the pandemic, ie COVID as well. In the final platform, this would further be supplemented with
    a calendar overview that provides predictive  insights a couple of months into the future; this will help the patient make a knowledgeable
    decision regarding the ideal time to submit a claim for the elective surgery.
    """

    st.sidebar.markdown("""
                        ## Patient
                        Basic details about the patient
                        """)
    age_group = st.sidebar.selectbox("Age group", age_groups)
    elective = st.sidebar.selectbox("Elective", electives)

    st.success(f"Visualizing patient approach for {elective} (age {age_group})")

    data = df.loc[(df.age == age_group) & (df.elective == elective), ['week', 'patients', 'physicians', 'claims']].set_index('week')
    st.line_chart(data, use_container_width=True)

    c = alt.Chart(data.reset_index()).mark_circle().encode(
        x='week', y='patients', size='claims', color='physicians', tooltip=['claims', 'physicians', 'patients']).interactive()
    st.altair_chart(c, use_container_width=True)

    f"### Covid vs. {elective} Correlation"

    covid = df.loc[(df.age == age_group) & (df.elective == "COVID"), ['week', 'patients', 'physicians', 'claims']].set_index("week")
    comparitive = pd.concat([covid.add_prefix("covid_"), data.add_prefix("elective_")], axis=1).dropna()

    "Following is the overlapping data that we have; we can plot a bivariate to see correlation change across time"
    st.dataframe(comparitive.head())
    try:
        fig = sns.pairplot(comparitive, kind='kde')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Cannot plot comparison {e}")

    "## Clinician"

    """
    This section gives you a function overview of the data visualization and rough interaction between a clinician administration
    and the platform. Essentially, the clinic/hospital can enter basic information regarding

    - in-patient vs out-patient
    - coverage scheme
    - state wise vs aggregate

    and will be presented with a dashboard of visualizations that highlight the change in, ie, prioritization/de-prioritization
    of various elective surgeries across their branches (ie, across states) across various age groups, with respect to COVID.
    In the final platform, this would further be supplemented with
    a calendar overview that provides predictive  insights a couple of months into the future; this will help the clinician make efficient decisions
    regarding the best way to prioritize different elective surgeries to optimally utilize their resources.
    """

    # TODO add clinician visualization here


if __name__ == "__main__":
    main()
