const info = await eda.dmt_Board.getCurrentBoardInfo();
return { keys: Object.keys(info), board: info, };
