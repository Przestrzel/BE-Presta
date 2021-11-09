<?php

/**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License version 3.0
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * @author    PrestaShop SA and Contributors <contact@prestashop.com>
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License version 3.0
 */

namespace PrestaShop\Module\Ps_metrics\Helper;

use InvalidArgumentException;
use PrestaShopLogger;

/**
 * @deprecated Use PrestaShop\Module\Ps_metrics\Adapter\LoggerAdapter instead
 */
class LoggerHelper
{
    /**
     * @deprecated Use PrestaShop\Module\Ps_metrics\Adapter\LoggerAdapter::log() instead
     *
     * @param string $message
     * @param int $severity
     *
     * @return void
     *
     * @throw InvalidArgumentException When severity exceeded allowed value of PrestaShop Logger implementation
     */
    public function addLog($message, $severity)
    {
        if (!is_int($severity) || $severity < 1 || $severity > 4) {
            throw new InvalidArgumentException(sprintf('Severity must be a positive integer between 1 and 4, %s given.', var_export($severity, true)));
        }

        PrestaShopLogger::addLog($message, $severity);
    }
}
