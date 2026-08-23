import { Request, Response, NextFunction } from "express"

const routeHandler = (
    route: (req: Request, res: Response, next: NextFunction) => Promise<any>
) => (
    req: Request, res: Response, next: NextFunction
) =>
    Promise.resolve(route(req, res, next)).catch(next)

export default routeHandler;