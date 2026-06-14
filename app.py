from src.database.database import (
    create_database,
    save_story,
    search_story
)

import streamlit as st

from src.data_collection.collector import load_feedback
from src.data_collection.consent_manager import filter_consent

from src.preprocessing.anonymizer import anonymize_data
from src.preprocessing.cleaner import clean_text

from src.templates.story_templates import (
    social_story,
    blog_story,
    case_study
)

from src.review_system.review import approve_story

from src.database.database import (
    create_database,
    save_story
)


# Create database
create_database()


st.title("AI Impact Story Generator")


file = st.file_uploader(
    "Upload Participant Feedback CSV"
)


if file:

    # ---------------- DATA COLLECTION ----------------

    data = load_feedback(file)

    st.subheader("Raw Feedback")

    st.dataframe(data)



    # ---------------- CONSENT ----------------

    data = filter_consent(data)



    # ---------------- PREPROCESSING ----------------

    data = clean_text(data)

    anonymous_data = anonymize_data(data)


    st.subheader("Anonymized Participant Data")

    st.dataframe(anonymous_data)



    # ---------------- STORY TYPE ----------------

    story_type = st.selectbox(
        "Choose Story Type",
        [
            "Social Media (50 words)",
            "Blog (200 words)",
            "Partner Case Study (500 words)"
        ]
    )



    # ---------------- SELECT PARTICIPANT ----------------

    participant = st.selectbox(
        "Select Participant",
        anonymous_data["skill"]
    )


    row = anonymous_data[
        anonymous_data["skill"] == participant
    ].iloc[0]



    # ---------------- STORY GENERATION ----------------

    if story_type == "Social Media (50 words)":

        story = social_story(
            row["skill"],
            row["experience"],
            row["impact"]
        )


    elif story_type == "Blog (200 words)":

        story = blog_story(
            row["skill"],
            row["experience"],
            row["impact"]
        )


    else:

        story = case_study(
            row["skill"],
            row["experience"],
            row["impact"]
        )



    st.subheader("Generated Story")

    st.write(story)



    # ---------------- HUMAN REVIEW ----------------

    st.subheader("Edit Story Before Approval")


    edited_story = st.text_area(
        "Modify story if required",
        story,
        height=250
    )



    choice = st.selectbox(
        "Review Status",
        [
            "Approve",
            "Reject"
        ]
    )



    if approve_story(choice):

        st.success(
            "Story approved for publication ✅"
        )


        # save approved story

        save_story(
            row["skill"],
            row["experience"],
            row["impact"],
            story_type,
            edited_story
        )


        st.info(
            "Story saved to database 💾"
        )


    else:

        st.warning(
            "Story needs revision"
        )
st.divider()


st.subheader("Search Story Repository 🔎")


keyword = st.text_input(
    "Search by Skill"
)


if keyword:

    results = search_story(keyword)

    if len(results) > 0:

        item = results[0]

        st.write("Skill:", item[0])

        st.write("Story Type:", item[1])

        st.write(item[2])

    else:

        st.warning("No stories found")
st.divider()

st.subheader("Task 7: AI Ethics & Privacy Guidelines")

st.markdown(
"""
### 🔐 Participant Consent

- Stories are generated only after explicit participant consent.
- Participants can withdraw permission for story usage.

### 🛡️ Data Privacy

- Personal information is anonymized before AI processing.
- Sensitive information is removed before story generation.

### 👤 Human Responsibility

- AI generated stories are reviewed by humans before publishing.
- Reviewers verify accuracy and avoid misleading information.

### 🤖 Responsible AI Usage

- AI assists storytelling but does not create fake achievements.
- Generated content must represent real participant experiences.

### 📢 Publishing Rules

- Only approved stories are stored in the repository.
- Participants control how their stories are shared.
"""
)