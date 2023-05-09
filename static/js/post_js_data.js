function post_data() {
    let elem = document.getElementById('food_select');
    console.log(lat)
    console.log(lng)
    elem.insertAdjacentHTML('afterend', `<input name="lat" value=${lat} type="hidden">`)
    elem.insertAdjacentHTML('afterend', `<input name="lng" value=${lng} type="hidden">`)

}

post_data()

function OnButtonClick() {
    target = document.getElementById("flex0");
    target.insertAdjacentHTML('afterend','<input type="submit" id="submit">')
    Submit = document.getElementById("submit");

    Submit.click()
}
