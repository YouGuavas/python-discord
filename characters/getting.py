import requests

async def get_chars(url, channel, character):
    page = requests.get(f"{url}accounts.php?rg_sess_id={character["session"]["session"]}&serverid={character["server_id"]}").text
    mains = page.split('characters on this server')[1].split("Trustee Access")[0].split("<tr>")
    trustees = page.split("Trustee Access")[1].split("</tbody>")[0].split("<tr>")
    main_chars = []
    trustee_chars = []
    for account in mains:
        if "suid" in account:
            suid = account.split("suid=")[1].split('&')[0]
            name = account.split("<b>")[1].split("</b>")[0]
            
            main_chars.append({"suid": suid, "name": name})
    for account in trustees:
        if "suid" in account:
            suid = account.split("suid=")[1].split('&')[0]
            name = account.split("<b>")[1].split("</b>")[0]

            trustee_chars.append({"suid": suid, "name": name})
    return [main_chars, trustee_chars]


