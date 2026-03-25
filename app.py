import streamlit as st
import aspose.words as aw
import img2pdf
import io

# --- SIDEBAR & PARTNERSHIP FORM ---
def setup_sidebar():
    with st.sidebar:
        st.title("pdftowordsimpleconverter")
        st.write("Free forever. No limits.")
        
        st.divider()
        
        # Affiliate / Ad Submission Form
        st.subheader("🤝 Work With Us")
        st.write("Become an affiliate or host an ad.")
        with st.form("partner_form", clear_on_submit=True):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            interest = st.selectbox("I want to:", ["Host an Ad", "Become an Affiliate", "Other"])
            details = st.text_area("Tell us more")
            submitted = st.form_submit_button("Submit Request")
            if submitted:
                # This shows a message to the user. 
                # (Later you can connect this to an email service)
                st.success("Request received! We'll contact you soon.")

# --- CONVERSION LOGIC ---
def run_conversion(file_bytes, source, target):
    in_stream = io.BytesIO(file_bytes)
    
    # Fast-path for JPEG to PDF
    if source == "JPEG" and target == "PDF":
        return img2pdf.convert(file_bytes)

    # General conversion using Aspose
    doc = aw.Document(in_stream)
    out_stream = io.BytesIO()
    
    formats = {
        "PDF": aw.SaveFormat.PDF,
        "WORD": aw.SaveFormat.DOCX,
        "JPEG": aw.SaveFormat.JPEG
    }
    
    doc.save(out_stream, formats[target])
    return out_stream.getvalue()

# --- MAIN INTERFACE ---
def main():
    st.set_page_config(page_title="pdftowordsimpleconverter", layout="centered")
    setup_sidebar()

    st.title("📄 pdftowordsimpleconverter")
    st.subheader("Convert Word, PDF, and JPEG in seconds.")

    # The 6 Requested Options
    choice = st.selectbox("Select conversion type:", [
        "Word to PDF", "PDF to Word", "JPEG to Word", 
        "JPEG to PDF", "Word to JPEG", "PDF to JPEG"
    ])

    src_label, _, tgt_label = choice.partition(" to ")
    
    # File upload mapping
    extensions = {"Word": ["docx", "doc"], "PDF": ["pdf"], "JPEG": ["jpg", "jpeg"]}
    uploaded_file = st.file_uploader(f"Upload your {src_label} file", type=extensions[src_label])

    if uploaded_file:
        if st.button(f"Convert to {tgt_label}"):
            with st.spinner("Converting..."):
                try:
                    result = run_conversion(
                        uploaded_file.getvalue(), 
                        src_label.upper(), 
                        tgt_label.upper()
                    )
                    st.success("Conversion Complete!")
                    st.download_button(
                        label=f"Download {tgt_label} File",
                        data=result,
                        file_name=f"converted_file.{tgt_label.lower() if tgt_label != 'Word' else 'docx'}",
                        mime="application/octet-stream"
                    )
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()
