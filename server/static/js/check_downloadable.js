// '다운로드 조회' 버튼을 누른 경우
$(function(){
    // 다운로드 가능 여부를 확인하고 해당 정보를 렌더링
    $('#submit-btn').on('click', function(){
        let send_url = $('#submit-btn').data('url');
        let youtube_url = $('#url').val();
        // 유튜브 주소를 입력하였는지 확인
        let is_content = check_form_content();
        if (is_content==false){
            // console.log('유튜브 주소를 입력하지 않았습니다.')
            alert('유튜브 주소를 입력하지 않았습니다.')
            return false
        } 
        delete_table_element(); // 기존 테이블 데이터 삭제
        $('#table-area').attr('hidden', true); // 테이블 숨기기 -> 검색이 끝나면 보이기
        $('#tumnail-link').attr('href', ''); // 썸네일 링크 초기화
        show_loading_img(); // Loading 이미지 시작
        hide_youtube_info();
        // console.log(youtube_url)
        // alert(1)
        $.ajax({
            method: 'post',
            url:send_url,
            contentType: "application/json",
            data: JSON.stringify(
                {'url': youtube_url}
            ),
            success: (data)=>{
                // console.log(data)
                // 비디오 리스트를 받아오면 표에 시현
                if (data.code==='200'){
                    append_table_element(data.files);
                    hide_loading_img(); // 로딩 이미지 숨기기
                    // console.log(data.title);
                    // console.log(data.thumbnail_url);
                    show_youtube_info(data.thumbnail_url, data.title, data.duration);
                    add_link_to_thumbnail(youtube_url); // 썸네일 이미지에 유튜브 링크 걸기
                    hide_result_table(); // 검색결과 테이블 보이기
                } else if (data.code==='400'){
                    alert('에러가 발생했습니다. 주소를 확인해 주세요')
                }
            },
            error:(error)=>{
                // console.log(error)
                alert('에러가 발생했습니다. 주소를 확인해 주세요');
                hide_loading_img(); // 로딩 이미지 숨기기
                clear_content();// 초기화 버튼
            }
        });
    });
});


function add_link_to_thumbnail(youtube_url){
    // 썸네일에 유튜브 링크 걸기
    $('#tumnail-link').attr('href', youtube_url);
}


function remove_link_to_thumbnail(){
    // 썸네일에 유튜브 링크 걸기
    $('#tumnail-link').attr('href', '');
}


function hide_result_table(){
    // 동영상 검색 결과 테이블 감추기
    $('#table-area').attr('hidden', false);
}

function check_form_content(){
    // 유튜브 주소창에 내용을 입력했는지 확인
    let youtube_url = $('#url').val();
    if (youtube_url == ''){return false}
    return true
}


function append_table_element(data){
    var type = {
        'mp4': 1,
        'm4a': 2,
        'mp3': 3,
        'optimal': 4,
    }
    // 최적 동영상 다운로드
    // 최적 도영상 size 찾기 -> id == 22
    let best_video_size = 0;
    for (x=0; x<data.length; x++){
        if (data[x]['files']['id'] == 22 ){
            best_video_size = data[x]['files']['size_mb']
        }
    }
    $('#video-list').append(
        `<tr class="file-list">
            <th>비디오(최적)</th>
            <td>mp4</td>
            <td style="color: red;">최고속도<br>강추!!</td>
            <td style="color: red;">최적해상도<br>(자동설정)</td>
            <td>
                <a href="#"
                    id="mp3"
                    class="download-item btn btn-outline-primary"
                    onclick="download_tube(${0}, ${22}, ${best_video_size}, ${type['optimal']})">받기</a>
            </td>
         <tr>`
    )
    // 일반 선택 옵션 추가 - 최대 5개만 보여주기
    let video_max_list = 3;
    if (video_max_list > data.length){
        video_max_list = data.length;
    }
    for(let x=0; x<data.length; x++){
        // console.log(data[x])
        let data_type = '';
        let extention = 'mp4';
        
        // let key = Object.keys(data[x])[0];
        // console.log(x, video_max_list)
        if (x > video_max_list && data[x].type === 'mp4'){
            continue;
        }

        if (data[x].type==='mp4'){
            data_type = '비디오';
        } else if (data[x].type==='m4a'){
            data_type = '오디오(MP4 음성만)';
            extention = 'm4a'
        } else {
            data_type = '알수 없음';
        }
        const file_size = Math.round(data[x].size_mb * 10)/10; // 파일 크기 -> 소수 첫째자리 변환
        const file_size_comma = file_size.toLocaleString('en-US');
        $('#video-list').append(
            `<tr class="file-list">
                <th>${data_type}</th>
                <td>${data[x].type}</td>
                <td>${file_size_comma} MB</td>
                <td>${data[x].resolution}</td>
                <td>
                    <a href="#"
                        id="down-index-${x}"
                        class="download-item btn btn-outline-primary"
                        onclick="download_tube(
                            ${x}, 
                            ${data[x].id}, 
                            ${file_size},  
                            ${type[data[x].type]}
                        )">받기</a>
                </td>
             <tr>`
        )
    }
    // MP3 변환 후 다운로드 하기 추가
    $('#video-list').append(
        `<tr class="file-list">
            <th>MP3 파일</th>
            <td>mp3</td>
            <td>서버 변환 후 다운<br>(용량 알수 없음)</td>
            <td>해당없음</td>
            <td>
                <a href="#"
                    id="mp3"
                    class="download-item btn btn-outline-primary"
                    onclick="download_tube(${0}, ${0}, ${0}, ${type.mp3})">받기</a>
            </td>
         <tr>`
    )
}


// function download_tube(index, file_size, type){
function download_tube(index, video_idx, file_size, type){
    // 선택된 유튜브 영상을 다운로드
    // console.log(`type: ${type}`)
    let send_url = $('#downloading').data('download-url'); // 다운로드 view url
    let youtube_url = $('#url').val();
    // console.log(`index: ${index}`)
    // console.log(`file_size: ${video_idx}`)
    show_loading_img();
    let data = {
        'index': index,
        'video_idx': video_idx,
        'url': youtube_url,
        'type': type,
        'file_size': file_size,
    }
    
    // mp4 파일을 mp3 변환에서 받을지 물어보기
    if (type == 3){
        let mp3_decision = ask_mp3_type(); 
        if (mp3_decision === false){
            hide_loading_img();
            return
        }
    }
    
    // 용량과 해상도를 선택해서 다운로드 할지 물어보기
    if (type == 1){
        let mp4_decision = ask_mp4_type(); 
        if (mp4_decision === false){
            hide_loading_img();
            return
        }
    }    
    
    $.ajax({
        method: 'post',
        url:send_url,
        contentType: "application/json",
        data: JSON.stringify(data),
        success: (data)=>{
            // console.log(data)
            // 비디오 리스트를 받아오면 표에 시현
            if (data.code==='200'){
                hide_loading_img(); // 로딩 이미지 숨기기
                let request_btn = $('#request-file-btn');
                let reqeust_file_url = request_btn.attr('href');
                let reqeust_file_url_update = `${reqeust_file_url}?file=${data.file_path}`;
                let decision = confirm('파일이 준비되었습니다. 다운로드 하시겠습니까?');
                if (decision){
                    location.href = reqeust_file_url_update;
                }
            }
            else{
                // 향후 추가될 예외처리 코드                
            }
        },

        error:(error)=>{
            // console.log(error)
        }
    });
}

function ask_mp3_type(){
    let decision = confirm(
        `바로 다운로드 가능한 음성파일은 m4a 형식입니다. mp3 파일로 변환해서 다운로드 받을 수 있습니다.
        \nmp3 로 변환하면 서버 처리 시간 때문에 오래 걸릴 수 있습니다.
        \n대용량 mp3 변환 시 1분 이상 대기하면 "내용 초기화" 버튼을 누르고 약 15초 이후에 다시 시도해 주시면 됩니다.^^.
        \n다운로드를 시작할까요?
        `
    )
    return decision
}


function ask_mp4_type(){
    let decision = confirm(
        `비디오(최적) 옵션을 선택하면 가장 빠르게 다운로드 할 수 있습니다..
        \n하지만, 크기와 해상도를 별도로 선택하셨습니다. 
        \n서버 처리 시간 때문에 오래 걸릴 수 있습니다 ㅠㅠ\n다운로드를 시작할까요?
        `
    )
    return decision
}


function clear_content(){
    $('#clear-btn').on('click', function(){
        hide_youtube_info();
        delete_table_element();
        hide_loading_img();
        $('#table-area').attr('hidden', true)
        $('#url').val('')
    });
}


function delete_table_element(){
    // 기존에 있던 테이블 목록 삭제
    let table_list = $('.file-list')
    for (let i=0; i<table_list.length; i++){
        table_list[i].remove()
    }
}

function show_loading_img(){
    // 로딩 이미지 보이기
    $('.loading').attr('hidden', false);
}

function hide_loading_img(){
    // 로딩 이미지 숨기기
    $('.loading').attr('hidden', true);
}


function show_youtube_info(thumbnail_url, title, duration){
    // 유튜브 썸네일/제목 영역 보이기
    $('#tube-info-area').attr('hidden', false);
    $('#tube-thumbnail').attr('src', thumbnail_url);
    $('#tube-title').text(`${title} (재생시간: ${duration})`);
}


function hide_youtube_info(){
    // 유튜브 썸네일/제목 영역 감추기
    $('#tube-info-area').attr('hidden', true);
}

function click_file_request_btn(){
    let href = $('#request-file-btn').attr('href')
    // console.log(`click_file_request_btn >>> ${href}`)
    $('#request-file-btn').trigger('click');
}