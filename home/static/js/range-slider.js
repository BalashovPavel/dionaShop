const rangeSlider = document.getElementById('range-slider')
const min_price = parseInt(document.getElementById('min-price').value)
const max_price = parseInt(document.getElementById('max-price').value)

const min = parseInt(document.getElementById('id_price_0').value)
const max = parseInt(document.getElementById('id_price_1').value)


if (rangeSlider) {
    if (isNaN(min) || isNaN(max)) {
        noUiSlider.create(rangeSlider, {
            start: [min_price, max_price],
            connect: true,
            step: 1,
            range: {
                'min': [min_price],
                'max': [max_price]
            }
        });
    } else {
        noUiSlider.create(rangeSlider, {
            start: [min, max],
            connect: true,
            step: 1,
            range: {
                'min': [min_price],
                'max': [max_price]
            }
        });
    }


    const input0 = document.getElementById('id_price_0')
    const input1 = document.getElementById('id_price_1')
    const inputs = [input0, input1]

    const rangeinput0 = document.getElementById('range-input-0');
    const rangeinput1 = document.getElementById('range-input-1');
    const rangeinputs = [rangeinput0, rangeinput1];

    rangeSlider.noUiSlider.on('update', function (values, handle) {
        rangeinputs[handle].value = Math.round(values[handle]);
        inputs[handle].value = Math.round(values[handle]);
        // input0 = rangeinput0.value
        // input1 = rangeinput1.value
    })


    const setRangeSlider = (i, value) => {
        let arr = [null, null];
        arr[i] = value;
        rangeSlider.noUiSlider.set(arr)
    };

    rangeinputs.forEach((el, index) => {
        el.addEventListener('change', (e) => {
            setRangeSlider(index, e.currentTarget.value);
        });
    });

}
