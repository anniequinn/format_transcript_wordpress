import streamlit as st
import re
import base64


def convert_md_to_wp(input_data, interviewer, interviewee):
    pattern_interviewee = re.compile(rf"{interviewee}: (.*?)\n", re.DOTALL)
    pattern_interviewer = re.compile(rf"{interviewer}: (.*?)\n", re.DOTALL)

    wp_format_interviewee = (
        "<!-- wp:paragraph -->\n<p>{}</p>\n<!-- /wp:paragraph -->\n"
    )
    wp_format_interviewer = '<!-- wp:ultimate-post/heading {{"blockId":"6c21a9","headingText":"{}","headingStyle":"style6","headingBorderBottomColor":"#f52900"}} /-->\n'  # noqa: E501

    output_data = re.sub(
        pattern_interviewee,
        lambda m: wp_format_interviewee.format(m.group(1).strip()),
        input_data,
    )
    output_data = re.sub(
        pattern_interviewer,
        lambda m: wp_format_interviewer.format(m.group(1).strip()),
        output_data,
    )

    return output_data


st.title("Format interview transcript for WordPress")

# Text input for the interview transcript
transcript = st.text_area("Paste the interview transcript here:", height=250)

# Text input for the interviewer and interviewee tags
interviewer_tag = st.text_input("Enter the interviewer tag:")
interviewee_tag = st.text_input("Enter the interviewee tag:")

# Button to trigger the conversion
if st.button("Convert"):
    if transcript and interviewer_tag and interviewee_tag:
        # Perform the conversion
        result = convert_md_to_wp(transcript, interviewer_tag, interviewee_tag)

        # Display the result and create a download link
        st.write("Conversion successful! Here is the output:")
        # st.code(result)
        st.text_area("", value=result, height=300, key="output_area")

        b64 = base64.b64encode(
            result.encode()
        ).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:text/plain;base64,{b64}" download="formatted_intvw_transcript.txt" target="_blank">Download</a>'  # noqa: E501
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.write("Please fill in all fields before clicking 'Convert'.")
