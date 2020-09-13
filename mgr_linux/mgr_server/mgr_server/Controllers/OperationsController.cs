﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using mgr_server.State;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace mgr_server.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class OperationsController : ControllerBase
    {
        private static readonly object lockA = new object();
        private static readonly object lockB = new object();
        private static readonly object lockC = new object();
        private static Dictionary<string, object> lockDict = new Dictionary<string, object>();

        private readonly ILogger<OperationsController> _logger;
        private OperationsTimes _operationsTimes;

        public OperationsController(ILogger<OperationsController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        [Route("A/{input}/{sleep}")]
        public string GetA(string input, int sleep)
        {
            lock (lockA)
            {
                Thread.Sleep(sleep);
                return input.ToUpper();
            }
        }

        [HttpGet]
        [Route("B/{input}/{sleep}")]
        public int GetB(int input, int sleep)
        {
            lock (lockB)
            {
                Thread.Sleep(sleep);
                return input * -1;
            }
        }

        [HttpGet]
        [Route("C/{input}/{sleep}")]
        public float GetC(int input, int sleep)
        {
            lock (lockC)
            {
                Thread.Sleep(sleep);
                if (input == 0)
                {
                    return int.MaxValue;
                }
                return 1 / input;
            }
        }

        [HttpGet]
        [Route("D/{input}/{sleep}")]
        public int GetD(int input, int sleep)
        {
            lock (lockC)
            {
                Thread.Sleep(sleep);
                return (new Random()).Next();
            }
        }

        [HttpGet]
        [Route("0/{input}/{sleep}")]
        public int Get0(string input, int sleep)
        {
            lockDict.TryAdd(input, new object());
            lock (lockDict[input])
            {
                Thread.Sleep(sleep);
                return (new Random()).Next();
            }
        }
    }
}
