
function setLocation(pos) {
	// 緯度・経度を取得
	lat = pos.coords.latitude;
	lng = pos.coords.longitude;

}
// エラー時に呼び出される関数
function showErr(err) {
	switch (err.code) {
		case 1: alert("位置情報の利用が許可されていません.札幌駅を現在地として案内します"); break;
		case 2: alert("デバイスの位置が判定できません"); break;
		case 3: alert("タイムアウトしました"); break;
		default: alert(err.message);
	}
}

//取得失敗時のデフォルト（札幌駅）
var lat = 43.06870648766271;
var lng = 141.35083599271363;
// geolocation に対応しているか否かを確認
if ("geolocation" in navigator) {
	var opt = {
		"enableHighAccuracy": true,
		"timeout": 10000,
		"maximumAge": 0,
	};
	navigator.geolocation.getCurrentPosition(setLocation, showErr, opt);
} else {
	alert("ブラウザが位置情報取得に対応していません");
}
