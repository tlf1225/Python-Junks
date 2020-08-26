const canvas = document.querySelector('#display');
const canvasContext = canvas.getContext('2d');
canvas.width = 1280;
canvas.height = 480;

// 音楽ファイルをdataURLに変換する
// Promiseを返す
async function convertAudioFileToDataUrl(file) {
  const reader = new FileReader();

  const loadPromise = new Promise((resolve, reject) => {
    reader.onload = (event) => {
      resolve(event.target.result);
    };
  });

  reader.readAsDataURL(file);

  return loadPromise;
}

// canvasにスペクトラムバーを描画する
function render(spectrum) {
  // canvasの幅を均等に割り振る
  const barWidth = Math.round(canvas.width / spectrum.length);

  // 色は黒
  canvasContext.fillStyle = 'rgba(100, 210, 240, 0.9)';

  // 前の描画を消す
  canvasContext.clearRect(0, 0, canvas.width, canvas.height);
  for(let i = 0; i < spectrum.length; i++) {
    // 四角形の描画
    // fillRectは本来左上から幅と高さを指定するが、ここでは左下から指定している
    // やり方は簡単で、高さ（スペクトラムの値）をマイナスにするだけ
    canvasContext.fillRect((barWidth + 1) * i, canvas.height, barWidth, -(spectrum[i] * (canvas.height)) / 255 + 10);
  }
}

// ファイルが選択されたら
const fileInput = document.getElementById("file-input");
const link = document.getElementById("link");

let audio = null;
let audioSource = null;
let intervalId = null;

fileInput.addEventListener('change', async (event) => {
  // Web Audio API周りの準備
  const audioContext = new AudioContext();
  const analyzerNode = audioContext.createAnalyser(); // 音分析ノード

  // 2回目以降のときは、前のオーディとタイマーを破棄してから処理にうつる
  if(audio) {
    audio.pause();
    audio.src = '';
  }

  if(audioSource) {
    audioSource.disconnect();
  }

  if(intervalId) {
    clearInterval(intervalId);
  }

  // FFTのウィンドウサイズ
  // 値は2の累乗（2, 4, 8, 16, 32, ...）
  analyzerNode.fftSize = 512;

  const file = fileInput.files[0];
  if(file) {
    // スペクトラムを保持するUint8Arrayを用意
    // サイズはfftSizeの半分（＝frequencyBinCount）
    const spectrumArray = new Uint8Array(analyzerNode.frequencyBinCount);

    // 選択されたファイルをdataURLにしてaudio要素に突っ込む
    audio = new Audio();
    audio.src = await convertAudioFileToDataUrl(file);
    audio.loop = true;

    // 選択ファイル -> 分析ノード -> 出力（スピーカー）
    // の順でつなぐ
    audioSource = audioContext.createMediaElementSource(audio);
    audioSource.connect(analyzerNode);
    analyzerNode.connect(audioContext.destination);

    // 定期的に値を見て描画する
    // requestAnimationFrameでもok
    intervalId = setInterval((event) => {
      // ノードから周波数データを取り出す
      analyzerNode.getByteFrequencyData(spectrumArray);

      // 描画する
      render(spectrumArray);
    }, 1/60);

    // 再生開始
    audio.play();
  }
});

link.addEventListener('keypress', (evt) => {
  if(evt.keyCode == 13) {
  const audioContext = new AudioContext();
  const analyzerNode = audioContext.createAnalyser(); // 音分析ノード

  // 2回目以降のときは、前のオーディとタイマーを破棄してから処理にうつる
  if(audio) {
    audio.pause();
    audio.src = '';
  }

  if(audioSource) {
    audioSource.disconnect();
  }

  if(intervalId) {
    clearInterval(intervalId);
  }

  // FFTのウィンドウサイズ
  // 値は2の累乗（2, 4, 8, 16, 32, ...）
  analyzerNode.fftSize = 512;

  // スペクトラムを保持するUint8Arrayを用意
  // サイズはfftSizeの半分（＝frequencyBinCount）
  const spectrumArray = new Uint8Array(analyzerNode.frequencyBinCount);

  audio = new Audio();
  audio.src = link.value;
  audio.loop = true;

  // 選択ファイル -> 分析ノード -> 出力（スピーカー）
  // の順でつなぐ
  audioSource = audioContext.createMediaElementSource(audio);
  audioSource.connect(analyzerNode);
  analyzerNode.connect(audioContext.destination);

  intervalId = setInterval((event) => {
    analyzerNode.getByteFrequencyData(spectrumArray);
    render(spectrumArray);
  }, 1/60);
  audio.play();
  }
});