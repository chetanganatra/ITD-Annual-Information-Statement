# ITD AIS JSON Decrypt & Excel Converter

Python and HTML scripts to decrypt the Income Tax Department's Annual Information Statement (AIS) JSON and convert it into Excel for easier analysis!

---

1. **Download Encrypted AIS JSON**  
   - Login to the [Income Tax e-Filing portal](https://eportal.incometax.gov.in/)  
   - Download `Annual Information Statement (AIS) - JSON (for AIS Utility)`

2. **Decrypt JSON**  
   - Open `1.Extract-JSON-From-Encrypted-AIS.html` in a browser  
   - Upload the encrypted file & enter your password (PAN in lowercase + DOB in ddmmyyyy format)  
   - Save the decrypted JSON to a new file (e.g., `clean.json`) 

3. **Convert to Excel**
   
   Run the Python script:
   ```bash
   pip install -r requirements.txt
   python 2.Convert-AIS-Clean-Json-to-Excel.py clean.json
   ```
   This will generate clean.xlsx in the same folder.

## Disclaimers

- Scripts are provided **as-is** with no warranties.  
- Use them at your own risk; the author is not responsible for any issues or data loss.  
- Adapt the code to fit your environment before production use.
- `Do not upload or share your decrypted AIS JSON publicly. Keep your tax data private.`

## License
This project is licensed under the [MIT License](LICENSE).  
