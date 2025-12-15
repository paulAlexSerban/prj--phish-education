const puppeteer = require('puppeteer');

async function takeScreenshot() {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.error('Usage: node screenshot.js <URL> <output-filename>');
    process.exit(1);
  }

  const url = args[0];
  const outputPath = args[1];

  // Add protocol if missing
  if (!url.match(/^https?:\/\//i)) {
    url = 'https://' + url;
    console.log(`Protocol not found, using: ${url}`);
  }

  console.log(`Taking screenshot of: ${url}`);
  console.log(`Output: ${outputPath}`);

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || '/usr/bin/chromium',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--ignore-certificate-errors',
      '--disable-web-security',
      '--disable-gpu'
    ]
  });

  try {
    const page = await browser.newPage();
    
    // Set viewport size
    await page.setViewport({
      width: 1920,
      height: 1080,
      deviceScaleFactor: 1,
    });

    // Navigate to the URL
    await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: 60000
    });

    // Take screenshot
    await page.screenshot({
      path: outputPath,
      fullPage: false,
      type: 'png'
    });

    console.log(`Screenshot saved to: ${outputPath}`);
  } catch (error) {
    console.error('Error taking screenshot:', error);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

takeScreenshot();
