<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router'
    import { page, keyword, is_login } from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    let question_list = []
    let size = 10
    let total = 0
    let kw = ''
    $: total_page = Math.ceil(total/size)

    function get_question_list() {
        let params = {
            page: $page,
            size: size,
            keyword: $keyword,
        }

        fastapi('get', '/api/question/list', params, (json) => {
            question_list = json.question_list
            total = json.total
            kw = $keyword
        })
    }

    /*  $: 변수1, 변수2, 자바스크립트식 과 같이 사용하면 스벨트는 "변수1" 또는 "변수2"의 값이 변경되는지를 감시하다가
        값이 변경되면 자동으로 "자바스크립트식"을 실행한다.  */
    $: $page, $keyword, get_question_list()
</script>

<div class="container my-3">
    <div class="row my-3">
        <div class="col-6">
            <a use:link href="/question-create"
                class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a>
        </div>
        <div class="col-6">
            <div class="input-group">
                <input type="text" class="form-control" bind:value="{kw}">
                <button class="btn btn-outline-secondary" on:click={() => {$keyword = kw, $page = 0}}>찾기</button>
            </div>
        </div>
    </div>
    <table class="table">
        <thead>
        <tr class="text-center table-dark">
            <th>번호</th>
            <th style="width:50%">제목</th>
            <th>글쓴이</th>
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        {#each question_list as question, i}
        <tr>
            <td class="text-center">{ total - ($page * size) - i }</td>
            <td>
                <a use:link href="/detail/{question.id}">{question.subject}</a>
                {#if question.answers.length > 0}
                <span class="text-danger small mx-2">[{question.answers.length}]</span>
                {/if}
            </td>
            <td class="text-center">{question.user ? question.user.username : ""}</td>
            <!-- hh: 시간(0~12시), a: 오전, 오후-->
            <td class="text-center">{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>  
        </tr>
        {/each}
        </tbody>
    </table>
    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => $page--}">이전</button>
        </li>
        <!-- 페이지번호 -->
        {#each Array(total_page) as _, loop_page(loop_page)}
        {#if loop_page >= $page-2 && loop_page <= $page+2} 
        <li class="page-item {loop_page === $page && 'active'}">
            <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
        </li>
        {/if}
        {/each}
        <!-- 다음페이지 -->
        <li class="page-item {$page >= total_page-1 && 'disabled'}">
            <button class="page-link" on:click="{() => $page++}">다음</button>
        </li>
    </ul>
    <!-- 페이징처리 끝
    <a use:link href="/question-create"
        class="btn btn-primary {$is_login ?'' : 'disabled'}">질문 등록하기</a>
    -->
</div>