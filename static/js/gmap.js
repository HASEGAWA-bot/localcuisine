let origin = [];
let ori = new Object();
let destinations = [];

ori.lat = markerData[0].lat;
ori.lng = markerData[0].lng;
origin.push(ori);

for (let i = 1; i < markerData.length; i++) {
	let des = new Object();
	des.lat = markerData[i].lat;
	des.lng = markerData[i].lng;
	destinations.push(des);
}
console.log(origin);
console.log(JSON.stringify(destinations));

var map;
var marker = [];
var infoWindow = [];
var iconloc = '/static/img/pin.png';
var iconnow = '/static/img/home.png';

function initMap() {
	//ここから、距離行列
	const DistMatrix = new google.maps.DistanceMatrixService();
	// instantiate Distance Matrix DistMatrix
	const matrixOptions = {
		origins: origin,
		destinations: destinations,
		travelMode: 'WALKING',
	};
	// Call Distance Matrix DistMatrix
	DistMatrix.getDistanceMatrix(matrixOptions, callback);

	let routes = new Object();
	// Callback function used to process Distance Matrix response
	function callback(response, status) {
		if (status !== "OK") {
			alert("There is no restaurants around here");
			return;
		}
		console.log(response);

		routes = response.rows[0].elements;
		const place = document.getElementById('under');

		//逆順になる
		for (let i = 0; i < routes.length; i++) {
			const accesstime = routes[i].duration.text;
			place.insertAdjacentHTML('afterend', `<p class="accesstime"> To ${markerData[i + 1].name} ,it takes<big> ${accesstime} </big> by walk</p>`);
		}
	}
	// 地図の作成
	let mapLatLng = new google.maps.LatLng({ lat: markerData[0]['lat'], lng: markerData[0]['lng'] }); // 緯度経度のデータ作成
	map = new google.maps.Map(document.getElementById('map'), {
		center: mapLatLng, // 地図の中心を指定
		zoom: 16 // 地図のズームを指定
	});

	// マーカー毎の処理
	for (let i = 0; i < markerData.length; i++) {
		markerLatLng = new google.maps.LatLng({ lat: markerData[i]['lat'], lng: markerData[i]['lng'] }); // 緯度経度のデータ作成
		marker[i] = new google.maps.Marker({ // マーカーの追加
			position: markerLatLng, // マーカーを立てる位置を指定
			map: map // マーカーを立てる地図を指定
		});
	}

	for (let i = 1; i < markerData.length; i++) { // restaurant's icon
		marker[i].setOptions({
			icon: {
				url: iconloc
			}
		});
		const contentstr = `<div class="info"><p font-size: 24px;>店名<a href="${markerData[i]['url']}">${markerData[i]['name']}</a><br>MENU:${markerData[i]['menu']}</p></div>`

		infoWindow[i] = new google.maps.InfoWindow({ // 吹き出しの追加
			content: contentstr
		});

		infoWindow[i].open(map, marker[i]); // 吹き出しの表示
		markerEvent(i);


	}

	marker[0].setOptions({// current location's icon
		icon: {
			url: iconnow
		}
	});
	infoWindow[0] = new google.maps.InfoWindow({ // 吹き出しの追加
		content: '<div class="info">you are HERE! </div>' // 吹き出しに表示する内容
	});

	infoWindow[0].open(map, marker[0]); // 吹き出しの表示
	markerEvent(0);

}
// マーカーにクリックイベントを追加
function markerEvent(i) {
	marker[i].addListener('click', function () { // マーカーをクリックしたとき
		infoWindow[i].open(map, marker[i]); // 吹き出しの表示
	});
}