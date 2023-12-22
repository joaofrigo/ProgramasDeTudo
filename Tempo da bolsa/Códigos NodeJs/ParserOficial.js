import request from 'request';
import * as fs from "fs";

function ColocaVirgulas(stringo)
{
  stringo = stringo.split('');
  stringo = stringo.toString();
  return stringo;
}

function VerificaInicio(posicao, inicio, body)
{
  var i;
  var frase = [];
  for (i = 0; i<inicio.length; i++) {
    frase[i] = body[posicao + i];
  }
  frase = frase.toString();
  inicio = ColocaVirgulas(inicio);
  if (frase == inicio) {
    return true;
  }
  else {
    return false;
  }

}

  function VerificaFim(posicao, fim, body)
{
  var i;
  var frase = [];
  for (i = 0; i<fim.length; i++) {
    frase[i] = body[posicao + i];
  }
  frase = frase.toString();
  fim = ColocaVirgulas(fim);
  if (frase == fim) {
    return true;
  }
  else {
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
      if (VerificaFim(i+posicao, fim, body)) {
        return parsed;
      }
    }
    i++;
  }
  return parsed;
}

main();

function main() {
var dia;
dia = 20220101;
var URL = "exemplo.com/";
//////////////////////
var existe = request("exemplo.com/", function (error, response, body) {
    if (existe == undefined) {
      console.log("O request falhou");
      return;
    }
    const fim = "</script>";
    const inicio = "var json_data";
    var buffer;
    var i = 0;
    var parsed;
    while(1) {
      buffer = body[i];
      if (buffer == inicio[0]) {
        if (VerificaInicio(i, inicio, body)) {
          parsed = PegaParsed(i, fim, body);
          parsed = parsed.join('');
          break;
        }
      }
      if (buffer == undefined) {
        break;
      }
      i++;
    }
    var NomeArquivo = ["Arquivo JSON do dia ", dia];
    NomeArquivo = NomeArquivo.join("");
    fs.writeFile(NomeArquivo, parsed, (err) => {
      if (err)
      console.log ("não foi");
      else {
        console.log("O arquivo foi escrito com sucesso");
      }
      });
})
}