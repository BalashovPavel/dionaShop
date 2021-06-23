let select = function () {
    let selectHeader = document.querySelectorAll('.select-catalog__header');
    let selectItem =document.querySelectorAll('.select-catalog__item');

    selectHeader.forEach(item=>{
        item.addEventListener('click', selectToggle)
    });

    selectItem.forEach(item=>{
        item.addEventListener('click', selectToggle)
    });

    function selectToggle() {
        this.parentElement.classList.toggle('is-active')
    }

    function  selectChoose() {
        let text = this.innerText,
            select = this.closest('.select-catalog'),
            currentText = select.querySelector('.select-catalog__current');
        currentText.innerText = text;
        select.classList.remove('is-active')
    }
}

select()