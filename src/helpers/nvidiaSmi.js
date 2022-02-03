// Borrowed and modified from https://github.com/sebhildebrandt/systeminformation/blob/master/lib/graphics.js
// Changed to be asynchronous to avoid blocking

import fs from 'fs/promises';
import os from 'os';

let nvidiaSmiPath;

// Best approximation of what drive windows is installed on
const homePath = os.homedir();
const WINDIR = homePath ? `${homePath.charAt(0)}:\\Windows` : 'C:\\Windows';

const asyncFilter = async (arr, predicate) => Promise.all(arr.map(predicate))
  .then((results) => arr.filter((_v, index) => results[index]));

export const getNvidiaSmi = async () => {
  if (nvidiaSmiPath) {
    return nvidiaSmiPath;
  }

  if (os.platform() === 'win32') {
    try {
      const basePath = `${WINDIR}\\System32\\DriverStore\\FileRepository`;
      // find all directories that have an nvidia-smi.exe file
      const candidateDirs = await asyncFilter((await fs.readdir(basePath)), async (dir) => (await fs.readdir([basePath, dir].join('/'))).includes('nvidia-smi.exe'));
      // use the directory with the most recently created nvidia-smi.exe file
      const targetDir = candidateDirs.reduce(async (prevDir, currentDir) => {
        const awaitedPrevDir = await prevDir;
        const previousNvidiaSmi = (await fs.stat([basePath, awaitedPrevDir, 'nvidia-smi.exe'].join('/')));
        const currentNvidiaSmi = (await fs.stat([basePath, currentDir, 'nvidia-smi.exe'].join('/')));
        return (previousNvidiaSmi.ctimeMs > currentNvidiaSmi.ctimeMs) ? awaitedPrevDir : currentDir;
      });

      if (targetDir) {
        nvidiaSmiPath = [basePath, targetDir, 'nvidia-smi.exe'].join('/');
      }
    } catch (e) {
      // idk
    }
  } else if (os.platform() === 'linux') {
    nvidiaSmiPath = 'nvidia-smi';
  }
  return nvidiaSmiPath;
};

export const getSmiQuery = (delay) => `-lms ${delay} --query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu,utilization.memory --format=csv,noheader,nounits`;
