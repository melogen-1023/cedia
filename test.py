import requests

if __name__ == '__main__':
    res = requests.get(
        "https://api.bilibili.com/pgc/player/web/playurl?cid=154550798&qn=0&type=&otype=json&fourk=1&bvid=BV1w7411j7bs&ep_id=313123&fnver=0&fnval=80",
        headers={
            'cookie': "_uuid=3B872007-3CB9-1CC5-9A09-D3ED28E0639553737infoc; buvid3=331EC5D1-40B8-4B16-9A07-BDC4AD2D5C3518535infoc; sid=isc27ocb; fingerprint=d03134c24a729aac98b5cdd5e174a40d; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u))|R|JkYm0J'uYu|)Rl~kY; LIVE_BUVID=AUTO2116111019078638; fingerprint3=53fb32d6ff87b1f37b58afefdb6be059; fingerprint_s=fab07090719640bcc8d2249e43d520fa; buvid_fp=331EC5D1-40B8-4B16-9A07-BDC4AD2D5C3518535infoc; buvid_fp_plain=6921B0F7-9C0F-4EAA-9011-79163CCF3CFC155822infoc; DedeUserID=353064211; DedeUserID__ckMd5=bfefe483490ae151; SESSDATA=aaac2e56%2C1627312967%2C8ef63*11; bili_jct=8e15cc9b87a6ff98be41b565c9f2e749; bp_t_offset_353064211=485157688987752589; bp_video_offset_353064211=485186211865696789; PVID=12",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            'referer': 'https://www.bilibili.com/bangumi/play/ss32439/?from=search&seid=4189308348980619082'
        }
    )
    print(res.text)
