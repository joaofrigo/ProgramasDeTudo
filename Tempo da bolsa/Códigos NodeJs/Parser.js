import fetch from 'node-fetch';
import request from 'request';
import * as fs from "fs";
import * as async from 'async';
var diaAtual;

function ColocaVirgulas(stringo)
{
  //console.log ("A string é:", stringo);
  stringo = stringo.split('');
  //console.log("A string tomou split:", stringo, typeof(stringo));
  stringo = stringo.toString();
  //console.log("A string virou string:", stringo, typeof(stringo));
  return stringo;
}

function VerificaInicio(posicao, inicio, body)
{
  var i;
  //buffer[13] = body[posicao];
  var frase = [];
  //console.log(inicio.length, buffer, posicao);
  for (i = 0; i<inicio.length; i++) {
    frase[i] = body[posicao + i];
  }
  frase = frase.toString();
  inicio = ColocaVirgulas(inicio);
  //console.log ("A frase se formou:", frase, "O inicio é", inicio);
  if (frase == inicio) {
    //console.log ("O inicio foi encontrado");
    return true;
  }
  else {
    //console.log ("O inicio não foi encontrado");
    return false;
  }

}

  function VerificaFim(posicao, fim, body)
{
  var i;
  //buffer[13] = body[posicao];
  var frase = [];
  //console.log(fim.length, buffer, posicao);
  for (i = 0; i<fim.length; i++) {
    frase[i] = body[posicao + i];
  }
  frase = frase.toString();
  fim = ColocaVirgulas(fim);
  //console.log ("A frase se formou:", frase, "O fim é", fim);
  if (frase == fim) {
    //console.log ("O fim foi encontrado");
    return true;
  }
  else {
    //console.log ("O fim não foi encontrado");
    return false;
  }
}

function PegaParsed(posicao, fim, body) {
  var parsed, i;
  var buffer;
  parsed = [];
  i = 0;
  while(1) {
    buffer = body[i + posicao];
    parsed[i] = body[i + posicao];
    if (buffer == undefined) {
      return false;
    }
    if (buffer == fim[0]) {
      //console.log("mandando fim:", fim);
      if (VerificaFim(i+posicao, fim, body)) {
        //console.log("O fim foi encontrado");
        return parsed;
      }
    }
    i++;
  }
  return parsed;
}

main();

function retornaRequest()
{

}

function calculaDia(diaMarco0, diaFinal)
{
// primeiro preciso dar um parse nos valores dos anos dias e meses.
var arrayNumeros = diaMarco0.toString(10).split("").map(function(array){return parseInt(array)});
// ele pega o dia, transforma em string de decimais, dá um split (descobrindo o padrão dos numeros), depois vai em cada
// membro dessa string e transforma cada pequena string nesse array de strings em números de fato.
console.log("O array de números ficou ", arrayNumeros);
var ano, mes, dia;
ano = "" + arrayNumeros[0] + arrayNumeros[1] + arrayNumeros[2] + arrayNumeros[3];
mes = "" + arrayNumeros[4] + arrayNumeros[5];
dia = "" + arrayNumeros[6] + arrayNumeros [7];
console.log("O ano ficou como:", ano, "O mes ficou", mes, "O dia ficou", dia);
// se eu fizer assim terei que rever todas as regras de ano e afins.
while(1) {
  //if (mes == 02 && ) // pode ser usado para fevereiro
  if (mes > 0 && mes <= 12 && dia > 0 && dia <=30) { // isso não funfa ainda em meses como fevereiro
    break;
  }
  break;
}
//var dia = diaMarco0 / 

}

function main() {
// preciso arrumar o dia que quando é 00 ele não existe.
// dá pra fazer ele subtrair mais uma vez se um pre requisito não for cumprido.
// no caso um if que determine o Mes e Dia que vão ser variaveis separadas e depois concatenadas.
// implementar um try catch.
const diaMarco0 = 20200420; // o dia de inicio do dashboard
const diaFinal = 20200430; // o dia final do dashboard (nosso inicio)
diaAtual=diaFinal;
//while(diaMarco0 <= diaAtual) { // enquanto o dia atual for maior que o marco0, continuar criando arquivos.
calculaDia(diaMarco0, diaFinal);
var URL = [];
URL = ["exemplo.com/", diaAtual,".html"];
//console.log("A URL atual é: ", URL);
URL = URL.join('');
console.log("A URL atual é: ", URL);
//////////////////////
var existe = request(URL, function (error, response, body) {
  //console.log("O valor do request é: ", existe);
    if (existe == undefined) {
      console.log("O request falhou");
      return;
    }
    const fim = "</script>";
    const inicio = "var json_data";
    var buffer;
    var i = 0;
    var parsed;
    console.log("While começou.");
    while(1) {
      buffer = body[i];
      if (buffer == inicio[0]) { // v igual a v de "var Json_data"
        if (VerificaInicio(i, inicio, body)) {
          //console.log("inicio encontrado, pegando a frase.");
          parsed = PegaParsed(i, fim, body);
          //console.log("O valor do parsed é:", parsed);
          parsed = parsed.join(''); // ou "" funfa também, um argumento que define como o join deve ser feito, com ou sem vírgula
          break;
        }
      }
      //console.log(buffer);
      if (buffer == undefined) {
        //console.log(body); // o final é undefined.
        break;
      }
      i++;
    }
    //console.log("While terminou. o parsed ficou no final:", parsed);
    //const fr = require("fs");
    // agora vai criar uma file com o Json.
    var NomeArquivo = ["Arquivo JSON do dia ", diaAtual];
    NomeArquivo = NomeArquivo.join("");
    console.log("O nome do arquivo será: ", NomeArquivo);
    try {
    fs.writeFile(NomeArquivo, parsed, (err) => {
      if (err)
      console.log ("não foi");
      else {
        console.log("O arquivo foi escrito com sucesso");
      }
      });
    }
    catch {
      console.log("Opa");
      //fs.writeFile(NomeArquivo, "A data não existe");
    }
    /*fs.writeFile("books.txt", "ola data", (err) => {
      if (err)
        console.log(err);
      else {
        console.log("File written successfully\n");
        console.log("The written has the following contents:");
        console.log(fs.readFileSync("books.txt", "utf8"));
      }
    });*/
})
diaAtual--;
}
//}

function ExtracaoEscrita(PosicaoInicial)
{
  console.log("A posição inicial atual é:", PosicaoInicial);
}




async function FuncaoRequest() {
    const response = await fetch("https://ead06.proj.ufsm.br/nginx-stats/20230418.html");
    const body = await response;
    //console.log("response:", body);
    return response;
}