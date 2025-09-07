# ITD-Annual-Information-Statement

Scripts to automate extraction of Indian Income Tax - Annual Info Statement (AIS) encrypted JSON into Excel worksheets for quick reference and analysis!

---

## Step 1: Download encrypted JSON

Login to Indian Income Tax eFiling portal and download 'Annual Information Statement (AIS) - JSON (for AIS Utility)'

## Step 2: Decrypt JSON 

Open '1.Extract-JSON-From-Encrypted-AIS.html' and copy paste the encrypted file and provide valid password. Click Decrypt. Copy paste the decrypted content into a separate file.

## Step 3: Convert to Excel

Execute the python script '2.Convert-AIS-Clean-Json-to-Excel.py' by passing the above clean json as parameter. Once the script is executed it would create an Excel file with same name as that of the clean json file.

```

python 2.Convert-AIS-Clean-Json-to-Excel.py clean.json

```


## Disclaimers

- Scripts are provided **as-is** with no warranties.  
- Use them at your own risk; the author is not responsible for any issues or data loss.  
- Adapt the code to fit your environment before production use.  

## License
This project is licensed under the [MIT License](LICENSE).  
