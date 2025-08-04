let dislike_btn = document.querySelector('.disliker')
let dislike_btn_data = document.querySelector('.dislike')

let like_btn = document.querySelector('.liker')
let like_btn_data = document.querySelector('.like')



let data_btn = document.querySelector('.data').value

like_btn.addEventListener('click', function () {
    like_btn_data.value = data_btn
})


dislike_btn.addEventListener('click', function () {
    dislike_btn_data.value = data_btn
})

