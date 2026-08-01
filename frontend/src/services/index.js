/**
 * DarkTrust – Services barrel export
 *
 * Re-exports all service modules for clean imports.
 *
 * Usage:
 *   import { api } from '@/services';
 *   import api from '@/services/api';  // Direct import also works
 */

export { default as api } from './api';

// Future service modules will be exported here:
// export { default as authService }    from './authService';
// export { default as policyService }  from './policyService';
// export { default as auditService }   from './auditService';
// export { default as gatewayService } from './gatewayService';
// export { default as riskService }    from './riskService';
