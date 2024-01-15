/*
데이터 송수신을 위한 fastapi 함수이다. 서버와의 통신을 담당한다.
서버와의 HTTP 요청을 보내는 데 사용되는 fastapi 함수를 정의한다.

매개변수
operation: 데이터를 처리하는 방법, HTTP요청방식, 소문자만 사용 get, put, delete, post 등
url: 요청 url, 백엔드 서버의 호스트명 이후의 url만 전달  /api/question/list
params: 요청 데이터(매개변수)  {page: 1, keyword: "마크다운" }
success_callback: API호출 성공시 수행할 함수, 전달된 함수에는 API 호출시 리턴되는 json이 입력으로 주어진다.
failure_callback: API호출 실패시 수행할 함수 , 전달된 함수에는 오류 값이 입력으로 주어진다.

fastapi 함수가 수행하는 것
매개변수로 받은 정보를 기반으로 HTTP 요청 생성: operation(HTTP 요청 방식), url(요청 URL), params(요청 매개변수), success_callback(성공 시 콜백 함수), failure_callback(실패 시 콜백 함수) 등의 매개변수를 받아서 HTTP 요청을 생성합니다.

HTTP 요청 생성: 주어진 매개변수를 바탕으로 HTTP 요청을 생성합니다. GET 요청의 경우 쿼리 매개변수를 URL에 추가하고, POST, PUT, DELETE 등의 다른 요청 방식의 경우 요청 본문(body)에 매개변수를 JSON 문자열로 변환하여 포함시킵니다.

fetch API를 사용한 HTTP 요청 전송: fetch 함수를 사용하여 서버에 HTTP 요청을 보냅니다. 이 함수는 주어진 URL 및 옵션으로 HTTP 요청을 실행합니다.

응답 처리: 서버로부터의 응답에 대한 처리를 수행합니다. 응답 상태 코드를 확인하여 성공 또는 실패에 따라 적절한 동작을 수행하며, 성공 또는 실패 시에는 콜백 함수를 호출하거나 알림을 표시합니다.
*/
import qs from "qs"
import { access_token, is_login, username } from "./store"
import { get } from "svelte/store"
import { push } from "svelte-spa-router"

const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)

    if(operation === 'login'){
        method = 'post',
        content_type = 'application/x-www-form-urlencoded',
        body = qs.stringify(params)
    }

    const _access_token = get(access_token)
    if(_access_token){
        options.headers["Authorization"] = "Bearer " + _access_token
    }

    let _url = import.meta.env.VITE_SERVER_URL+url
    if(method === 'get') {
        _url += "?" + new URLSearchParams(params)
    }

    let options = {
        method: method,
        headers: {
            "Content-Type": content_type
        }
    }

    if (method !== 'get') {
        options['body'] = body
    }

    fetch(_url, options)
        .then(response => {
            if(response.status === 204){
                if(success_callback){
                    success_callback()
                }
                return
            }
            response.json()
                .then(json => {
                    if(response.status >= 200 && response.status < 300) {  // 200 ~ 299
                        if(success_callback) {
                            success_callback(json)
                        }
                    
                    // operation이 'login' 인 경우는 아이디 또는 비밀번호를 틀리게 입력했을 경우에 401 오류가 발생하므로 제외해야 한다.
                    }else if(operation != 'login' && response.status===401){    // token time out
                        access_token.set('')    
                        username.set('')
                        is_login.set(false)
                        alert('로그인이 필요합니다.')
                        push('/user-login')
                    }else {
                        if (failure_callback) {
                            failure_callback(json)
                        }else {
                            alert(JSON.stringify(json))
                        }
                    }
                })
                .catch(error => {
                    alert(JSON.stringify(error))
                })
        })
}

export default fastapi