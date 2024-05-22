const { createCanvas, loadImage } = require('canvas');
const GIFEncoder = require('gifencoder');
const fs = require('fs');
const path = require('path');

async function createGif(imageFolder, outputGif, delay = 500, lastFrameDelay = 2000) {
    try {
        console.log(`Criando GIF em ${outputGif}\n\n`);
        const encoder = new GIFEncoder(500, 500); // ajuste o tamanho conforme necessário
        const stream = fs.createWriteStream(outputGif);
        encoder.createReadStream().pipe(stream);

        encoder.start();
        encoder.setRepeat(0); // 0 para loop infinito
        encoder.setDelay(delay); // tempo entre frames em ms
        encoder.setQuality(10); // qualidade da imagem

        const files = fs.readdirSync(imageFolder).filter(file => /\.(png|jpg|jpeg)$/i.test(file)).sort();

        if (files.length === 0) {
            throw new Error('Nenhuma imagem encontrada no diretório especificado.');
        }

        let i = 0

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const currentDelay = i === files.length - 1 ? lastFrameDelay : delay;

            try {
                const img = await loadImage(path.join(imageFolder, file));
                const canvas = createCanvas(img.width, img.height);
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, img.width, img.height);
                encoder.setDelay(currentDelay);
                encoder.addFrame(ctx);
            } catch (error) {
                console.error(`Erro ao carregar a imagem ${file}:`, error);
            }
        }

        // for (const file of files) {
        //     try {
        //         i++
        //         const img = await loadImage(path.join(imageFolder, file));
        //         const canvas = createCanvas(img.width, img.height);
        //         const ctx = canvas.getContext('2d');
        //         ctx.drawImage(img, 0, 0, img.width, img.height);

        //         if(i == files.length){
        //             console.log(`Adicionando ${file} frame ${i} de ${files.length} ao GIF...`)
        //             encoder.setDelay(lastFrameDelay);
        //         }

        //         encoder.addFrame(ctx);
        //     } catch (error) {
        //         console.error(`Erro ao carregar a imagem ${file}:`, error);
        //     }
        // }

        encoder.finish();
        stream.on('close', () => {
            console.log(`GIF criado com sucesso em ${outputGif}`);
        });
    } catch (error) {
        console.error('Erro ao criar GIF:', error);
    }
}

const imageFolder = 'images'; // diretório com as imagens
const outputGif = '5x5.gif'; // caminho do arquivo de saída

createGif(imageFolder, outputGif, 250, 1000).catch(console.error);
